"""
Base Agent class - Foundation for all AI employees.
Each agent has:
- A role and mindset (loaded from MD file)
- An LLM backend (Anthropic, Gemini, OpenAI, etc.)
- Access to tools via MCP server
- Event-driven communication with other agents
"""
import asyncio
import json
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

from ..utils.config import MINDSETS_DIR, get_config
from ..utils.logger import get_agent_logger
from ..utils.events import EventBus, Event, EventType, event_bus


class AgentStatus(Enum):
    """Current status of an agent."""
    OFFLINE = "offline"
    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    DELEGATING = "delegating"
    REPORTING = "reporting"
    ERROR = "error"


class AgentRole(Enum):
    """Roles for AI employees."""
    CSO = "CSO"  # Chief Strategy Officer (Jarvis)
    RESEARCH_ANALYST = "Research Analyst"  # Alice
    PRODUCT_DESIGNER = "Product Designer"  # Pixel
    SOFTWARE_ENGINEER = "Software Engineer"  # Max
    MARKETING_STRATEGIST = "Marketing Strategist"  # Nova
    DATA_ANALYST = "Data Analyst"  # Quinn
    CUSTOMER_SUCCESS = "Customer Success"  # Riley
    CONTENT_CREATOR = "Content Creator"  # Sam


@dataclass
class TaskResult:
    """Result of a task execution."""
    success: bool
    output: str
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_seconds: float = 0.0
    tokens_used: int = 0
    agent_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "data": self.data,
            "error": self.error,
            "duration_seconds": self.duration_seconds,
            "tokens_used": self.tokens_used,
            "agent_name": self.agent_name,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class Task:
    """A task to be executed by an agent."""
    id: str
    description: str
    assigned_to: str
    assigned_by: str = "system"
    priority: int = 5  # 1-10, 10 being highest
    context: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    result: Optional[TaskResult] = None
    status: str = "pending"  # pending, in_progress, completed, failed


class BaseAgent(ABC):
    """
    Base class for all AI employee agents.
    
    Each agent has:
    1. Identity (name, role, mindset)
    2. LLM backend for reasoning
    3. Tools accessible via MCP
    4. Communication via event bus
    """

    def __init__(
        self,
        name: str,
        role: AgentRole,
        event_bus: EventBus = event_bus,
    ):
        self.name = name
        self.role = role
        self.status = AgentStatus.OFFLINE
        self.event_bus = event_bus
        self.logger = get_agent_logger(name)
        self.config = get_config()

        # Load mindset from MD file
        self.mindset = self._load_mindset()

        # Conversation history for context
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 50

        # Task queue
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.current_task: Optional[Task] = None
        self.completed_tasks: List[Task] = []

        # Stats
        self.total_tokens_used = 0
        self.total_tasks_completed = 0
        self.total_tasks_failed = 0
        self.uptime_start: Optional[datetime] = None

        # Tools registry
        self.tools: Dict[str, Callable] = {}

        # Subscribe to delegation events
        self.event_bus.subscribe(EventType.DELEGATION_REQUEST, self._handle_delegation)

    def _load_mindset(self) -> str:
        """Load the agent's mindset/persona from MD file."""
        mindset_file = MINDSETS_DIR / f"{self.name.lower()}.md"
        if mindset_file.exists():
            return mindset_file.read_text(encoding="utf-8")
        self.logger.warning(f"No mindset file found at {mindset_file}")
        return f"You are {self.name}, a {self.role.value} AI employee."

    def register_tool(self, name: str, func: Callable, description: str = "") -> None:
        """Register a tool that this agent can use."""
        self.tools[name] = func
        self.logger.debug(f"Registered tool: {name}")

    async def start(self) -> None:
        """Start the agent."""
        self.status = AgentStatus.IDLE
        self.uptime_start = datetime.now()
        self.logger.info(f"{self.name} ({self.role.value}) is now ONLINE")

        await self.event_bus.publish(Event(
            event_type=EventType.AGENT_ONLINE,
            source=self.name,
            data={"role": self.role.value, "status": self.status.value},
        ))

        # Start the main loop
        await self._main_loop()

    async def stop(self) -> None:
        """Stop the agent gracefully."""
        self.status = AgentStatus.OFFLINE
        self.logger.info(f"{self.name} is going OFFLINE")

        await self.event_bus.publish(Event(
            event_type=EventType.AGENT_OFFLINE,
            source=self.name,
            data={"total_tasks": self.total_tasks_completed},
        ))

    async def _main_loop(self) -> None:
        """Main agent loop - process tasks from queue."""
        while self.status != AgentStatus.OFFLINE:
            try:
                # Wait for a task with timeout (for heartbeat)
                try:
                    task = await asyncio.wait_for(
                        self.task_queue.get(),
                        timeout=self.config.heartbeat_interval,
                    )
                    await self._process_task(task)
                except asyncio.TimeoutError:
                    # Heartbeat
                    await self.event_bus.publish(Event(
                        event_type=EventType.HEARTBEAT,
                        source=self.name,
                        data={
                            "status": self.status.value,
                            "tasks_completed": self.total_tasks_completed,
                            "tokens_used": self.total_tokens_used,
                            "queue_size": self.task_queue.qsize(),
                        },
                    ))
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.status = AgentStatus.ERROR
                await self.event_bus.publish(Event(
                    event_type=EventType.AGENT_ERROR,
                    source=self.name,
                    data={"error": str(e)},
                ))
                await asyncio.sleep(5)
                self.status = AgentStatus.IDLE

    async def _process_task(self, task: Task) -> TaskResult:
        """Process a single task."""
        self.current_task = task
        task.status = "in_progress"
        self.status = AgentStatus.WORKING
        start_time = datetime.now()

        self.logger.info(f"Starting task: {task.description[:80]}...")

        await self.event_bus.publish(Event(
            event_type=EventType.TASK_STARTED,
            source=self.name,
            data={"task_id": task.id, "description": task.description},
        ))

        try:
            # Execute the task (implemented by each agent)
            result = await self.execute_task(task)
            result.agent_name = self.name
            result.duration_seconds = (datetime.now() - start_time).total_seconds()

            task.result = result
            task.status = "completed" if result.success else "failed"

            if result.success:
                self.total_tasks_completed += 1
                self.logger.info(f"Task completed in {result.duration_seconds:.1f}s")

                await self.event_bus.publish(Event(
                    event_type=EventType.TASK_COMPLETED,
                    source=self.name,
                    data={"task_id": task.id, "result": result.to_dict()},
                ))
            else:
                self.total_tasks_failed += 1
                self.logger.warning(f"Task failed: {result.error}")

                await self.event_bus.publish(Event(
                    event_type=EventType.TASK_FAILED,
                    source=self.name,
                    data={"task_id": task.id, "error": result.error},
                ))

            self.total_tokens_used += result.tokens_used
            self.completed_tasks.append(task)

        except Exception as e:
            result = TaskResult(
                success=False,
                output="",
                error=str(e),
                agent_name=self.name,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
            )
            task.result = result
            task.status = "failed"
            self.total_tasks_failed += 1
            self.logger.error(f"Task execution error: {e}")

        finally:
            self.current_task = None
            self.status = AgentStatus.IDLE

        return result

    async def assign_task(self, task: Task) -> None:
        """Add a task to this agent's queue."""
        await self.task_queue.put(task)
        self.logger.info(f"Task queued: {task.description[:60]}...")

        await self.event_bus.publish(Event(
            event_type=EventType.TASK_ASSIGNED,
            source=task.assigned_by,
            target=self.name,
            data={"task_id": task.id, "description": task.description},
        ))

    async def _handle_delegation(self, event: Event) -> None:
        """Handle delegation requests from other agents (mainly Jarvis)."""
        if event.target != self.name:
            return

        task = Task(
            id=event.data.get("task_id", f"delegated-{datetime.now().timestamp()}"),
            description=event.data.get("description", ""),
            assigned_to=self.name,
            assigned_by=event.source,
            priority=event.data.get("priority", 5),
            context=event.data.get("context", {}),
        )

        await self.assign_task(task)

    @abstractmethod
    async def execute_task(self, task: Task) -> TaskResult:
        """
        Execute a task. Must be implemented by each agent.
        This is where the agent's LLM is called and tools are used.
        """
        raise NotImplementedError

    @abstractmethod
    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """
        Call the agent's LLM backend.
        Each agent uses a different model/provider.
        """
        raise NotImplementedError

    def get_status_dict(self) -> Dict[str, Any]:
        """Get current status as a dictionary."""
        return {
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "current_task": self.current_task.description[:60] if self.current_task else None,
            "queue_size": self.task_queue.qsize(),
            "total_completed": self.total_tasks_completed,
            "total_failed": self.total_tasks_failed,
            "total_tokens": self.total_tokens_used,
            "uptime": str(datetime.now() - self.uptime_start) if self.uptime_start else "0",
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} role={self.role.value} status={self.status.value}>"

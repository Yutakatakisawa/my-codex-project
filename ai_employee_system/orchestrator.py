"""
Orchestrator - The main engine that runs the AI Employee System.
Sets up all agents, MCP servers, and starts the 24/7 operation loop.
"""
import asyncio
import signal
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .agents import (
    JarvisAgent, AliceAgent, PixelAgent, MaxAgent,
    NovaAgent, QuinnAgent, RileyAgent, SamAgent,
)
from .agents.base_agent import Task
from .mcp_servers.tool_registry import tool_registry
from .utils.config import get_config
from .utils.logger import setup_logger, get_agent_logger
from .utils.events import event_bus
from .utils.telegram import TelegramReporter
from .dashboard.app import app as dashboard_app, setup_dashboard_events

logger = get_agent_logger("Orchestrator")


class Orchestrator:
    """
    Main orchestrator that manages the entire AI Employee System.
    
    Setup flow:
    1. Initialize all 7 agents
    2. Setup MCP servers for each agent
    3. Register all employees under Jarvis
    4. Start the dashboard
    5. Start the Telegram reporter
    6. Enter the main operation loop
    """

    def __init__(self):
        self.config = get_config()
        setup_logger(self.config.log_level)

        # Initialize agents
        self.jarvis = JarvisAgent()
        self.alice = AliceAgent()
        self.pixel = PixelAgent()
        self.max = MaxAgent()
        self.nova = NovaAgent()
        self.quinn = QuinnAgent()
        self.riley = RileyAgent()
        self.sam = SamAgent()

        self.all_agents = [
            self.jarvis, self.alice, self.pixel, self.max,
            self.nova, self.quinn, self.riley, self.sam,
        ]

        # Telegram reporter
        self.telegram = TelegramReporter()

        # Running state
        self._running = False
        self._agent_tasks: List[asyncio.Task] = []

    def setup(self) -> None:
        """Setup all components."""
        logger.info("Setting up AI Employee System...")

        # Register employees under Jarvis
        for agent in self.all_agents:
            if agent != self.jarvis:
                self.jarvis.register_employee(agent)

        # Register MCP servers in the global registry
        for agent in self.all_agents:
            if hasattr(agent, "mcp_server"):
                tool_registry.register_server(agent.name, agent.mcp_server)

        # Setup dashboard event subscription
        setup_dashboard_events()

        logger.info("Setup complete. All agents registered.")

    async def start(self) -> None:
        """Start all agents and the system."""
        self._running = True
        self.setup()

        logger.info("=" * 60)
        logger.info("  AI EMPLOYEE SYSTEM - STARTING")
        logger.info("  7 AI Employees | 24/7 Operations")
        logger.info("=" * 60)

        # Start Telegram
        await self.telegram.start()

        # Start all agent MCP servers
        for agent in self.all_agents:
            if hasattr(agent, "mcp_server"):
                await agent.mcp_server.start()

        # Start all agents (each runs their own async loop)
        for agent in self.all_agents:
            task = asyncio.create_task(agent.start())
            self._agent_tasks.append(task)

        logger.info("All agents started successfully!")

    async def stop(self) -> None:
        """Gracefully stop all agents."""
        logger.info("Shutting down AI Employee System...")
        self._running = False

        # Stop all agents
        for agent in self.all_agents:
            await agent.stop()

        # Cancel agent tasks
        for task in self._agent_tasks:
            task.cancel()

        # Stop MCP servers
        for agent in self.all_agents:
            if hasattr(agent, "mcp_server"):
                await agent.mcp_server.stop()

        # Stop Telegram
        await self.telegram.stop()

        logger.info("All agents stopped. System shutdown complete.")

    async def submit_objective(self, objective: str, context: Optional[Dict] = None) -> str:
        """
        Submit a high-level objective to Jarvis.
        Jarvis will analyze, plan, and delegate to the team.
        
        Args:
            objective: The business objective or task
            context: Additional context
            
        Returns:
            Task ID for tracking
        """
        task_id = f"obj-{uuid.uuid4().hex[:8]}"
        task = Task(
            id=task_id,
            description=objective,
            assigned_to="Jarvis",
            assigned_by="Human",
            priority=8,
            context=context or {},
        )

        logger.info(f"Objective submitted to Jarvis: {objective[:80]}...")
        await self.jarvis.assign_task(task)

        return task_id

    def get_system_status(self) -> Dict[str, Any]:
        """Get the full system status."""
        return {
            "system": {
                "running": self._running,
                "agents_total": len(self.all_agents),
                "timestamp": datetime.now().isoformat(),
            },
            "jarvis": self.jarvis.get_status_dict(),
            "employees": {
                agent.name: agent.get_status_dict()
                for agent in self.all_agents
                if agent != self.jarvis
            },
            "mcp_servers": tool_registry.get_all_stats(),
        }


async def run_with_dashboard(orchestrator: Orchestrator) -> None:
    """Run the orchestrator with the web dashboard."""
    import uvicorn

    config = get_config()

    # Start the orchestrator
    await orchestrator.start()

    # Run the dashboard server
    server_config = uvicorn.Config(
        dashboard_app,
        host=config.dashboard.host,
        port=config.dashboard.port,
        log_level="warning",
    )
    server = uvicorn.Server(server_config)

    try:
        await server.serve()
    except asyncio.CancelledError:
        pass
    finally:
        await orchestrator.stop()

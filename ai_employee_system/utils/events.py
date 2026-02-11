"""
Event bus for inter-agent communication.
Allows agents to publish and subscribe to events.
"""
import asyncio
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, List, Optional
from enum import Enum


class EventType(Enum):
    """Types of events in the system."""
    # Task lifecycle
    TASK_CREATED = "task_created"
    TASK_ASSIGNED = "task_assigned"
    TASK_STARTED = "task_started"
    TASK_PROGRESS = "task_progress"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"

    # Agent lifecycle
    AGENT_ONLINE = "agent_online"
    AGENT_OFFLINE = "agent_offline"
    AGENT_BUSY = "agent_busy"
    AGENT_IDLE = "agent_idle"
    AGENT_ERROR = "agent_error"

    # Communication
    MESSAGE_SENT = "message_sent"
    DELEGATION_REQUEST = "delegation_request"
    DELEGATION_RESPONSE = "delegation_response"
    REPORT_GENERATED = "report_generated"

    # System
    SYSTEM_STATUS = "system_status"
    HEARTBEAT = "heartbeat"


@dataclass
class Event:
    """An event in the system."""
    event_type: EventType
    source: str  # Agent name
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    target: Optional[str] = None  # Specific agent, or None for broadcast


class EventBus:
    """Central event bus for agent communication."""

    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._global_subscribers: List[Callable] = []
        self._event_history: List[Event] = []
        self._max_history: int = 1000
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: EventType, callback: Callable) -> None:
        """Subscribe to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def subscribe_all(self, callback: Callable) -> None:
        """Subscribe to all events (for dashboard, logging, etc.)."""
        self._global_subscribers.append(callback)

    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers."""
        async with self._lock:
            self._event_history.append(event)
            if len(self._event_history) > self._max_history:
                self._event_history = self._event_history[-self._max_history:]

        # Notify specific subscribers
        callbacks = self._subscribers.get(event.event_type, [])
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                pass  # Don't let subscriber errors break the bus

        # Notify global subscribers
        for callback in self._global_subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception:
                pass

    def get_history(self, event_type: Optional[EventType] = None, limit: int = 50) -> List[Event]:
        """Get recent event history."""
        if event_type:
            filtered = [e for e in self._event_history if e.event_type == event_type]
            return filtered[-limit:]
        return self._event_history[-limit:]

    def get_agent_events(self, agent_name: str, limit: int = 50) -> List[Event]:
        """Get events for a specific agent."""
        filtered = [e for e in self._event_history if e.source == agent_name or e.target == agent_name]
        return filtered[-limit:]


# Global event bus singleton
event_bus = EventBus()

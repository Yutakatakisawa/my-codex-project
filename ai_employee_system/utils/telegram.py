"""
Telegram Integration
====================
Sends real-time reports from Jarvis and system status updates.
Allows monitoring the AI employee team from anywhere via Telegram.
"""
import asyncio
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from .config import get_config
from .logger import get_agent_logger
from .events import Event, EventType, event_bus

logger = get_agent_logger("Telegram")


class TelegramReporter:
    """
    Sends reports and notifications to Telegram.
    Jarvis uses this to keep the human operator informed 24/7.
    """

    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self):
        config = get_config()
        self.bot_token = config.telegram.bot_token
        self.chat_id = config.telegram.chat_id
        self.enabled = config.telegram.enabled
        self._message_queue: asyncio.Queue = asyncio.Queue()

        if self.enabled:
            # Subscribe to events
            event_bus.subscribe(EventType.REPORT_GENERATED, self._on_report)
            event_bus.subscribe(EventType.AGENT_ONLINE, self._on_agent_status)
            event_bus.subscribe(EventType.AGENT_OFFLINE, self._on_agent_status)
            event_bus.subscribe(EventType.AGENT_ERROR, self._on_agent_error)
            event_bus.subscribe(EventType.TASK_COMPLETED, self._on_task_event)
            event_bus.subscribe(EventType.TASK_FAILED, self._on_task_event)

    async def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
        """Send a message to the configured Telegram chat."""
        if not self.enabled:
            logger.debug(f"Telegram disabled. Message: {text[:100]}...")
            return False

        try:
            url = f"{self.BASE_URL}{self.bot_token}/sendMessage"
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json={
                    "chat_id": self.chat_id,
                    "text": text[:4096],  # Telegram message limit
                    "parse_mode": parse_mode,
                })
                response.raise_for_status()
                logger.debug("Telegram message sent")
                return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    async def send_status_report(self, team_status: Dict[str, Any]) -> None:
        """Send a formatted team status report."""
        lines = [
            "🏢 *AI Employee System - Status Report*",
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        # Jarvis status
        jarvis = team_status.get("jarvis", {})
        lines.append(f"👔 *Jarvis (CSO)*: {jarvis.get('status', 'unknown')}")
        lines.append("")

        # Employee statuses
        employees = team_status.get("employees", {})
        status_emojis = {
            "idle": "🟢",
            "working": "🔵",
            "thinking": "🟡",
            "error": "🔴",
            "offline": "⚫",
        }

        for name, status in employees.items():
            emoji = status_emojis.get(status.get("status", ""), "⚪")
            task_info = f" → {status['current_task']}" if status.get("current_task") else ""
            lines.append(
                f"{emoji} *{name}* ({status.get('role', '')}): "
                f"{status.get('status', 'unknown')}{task_info}"
            )
            lines.append(
                f"   Tasks: {status.get('total_completed', 0)} done | "
                f"Tokens: {status.get('total_tokens', 0):,}"
            )

        lines.append("")
        lines.append(f"👥 Total Employees: {team_status.get('total_employees', 0)}")

        await self.send_message("\n".join(lines))

    async def _on_report(self, event: Event) -> None:
        """Handle report events from Jarvis."""
        summary = event.data.get("summary", "")
        task_desc = event.data.get("task_description", "")

        message = (
            f"📊 *Task Report from Jarvis*\n\n"
            f"*Task:* {task_desc[:200]}\n\n"
            f"*Summary:*\n{summary[:3500]}"
        )
        await self.send_message(message)

    async def _on_agent_status(self, event: Event) -> None:
        """Handle agent online/offline events."""
        if event.event_type == EventType.AGENT_ONLINE:
            await self.send_message(
                f"✅ *{event.source}* is now ONLINE "
                f"({event.data.get('role', '')})"
            )
        elif event.event_type == EventType.AGENT_OFFLINE:
            await self.send_message(
                f"⛔ *{event.source}* went OFFLINE "
                f"(Completed {event.data.get('total_tasks', 0)} tasks)"
            )

    async def _on_agent_error(self, event: Event) -> None:
        """Handle agent error events."""
        await self.send_message(
            f"🚨 *ERROR* - {event.source}\n"
            f"Error: {event.data.get('error', 'Unknown')}"
        )

    async def _on_task_event(self, event: Event) -> None:
        """Handle task completion/failure events."""
        if event.event_type == EventType.TASK_COMPLETED:
            # Only report significant task completions to avoid spam
            pass
        elif event.event_type == EventType.TASK_FAILED:
            await self.send_message(
                f"⚠️ *Task Failed* - {event.source}\n"
                f"Error: {event.data.get('error', 'Unknown')[:500]}"
            )

    async def start(self) -> None:
        """Start the Telegram reporter."""
        if self.enabled:
            await self.send_message(
                "🚀 *AI Employee System Started*\n"
                "7 AI employees are now online and ready to work."
            )
            logger.info("Telegram reporter started")
        else:
            logger.info("Telegram reporter disabled (no bot token)")

    async def stop(self) -> None:
        """Stop the Telegram reporter."""
        if self.enabled:
            await self.send_message(
                "🛑 *AI Employee System Shutting Down*\n"
                "All AI employees are going offline."
            )

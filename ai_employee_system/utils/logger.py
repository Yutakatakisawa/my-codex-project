"""
Logging setup for AI Employee System.
Uses loguru for structured, colorful logging.
"""
import sys
from pathlib import Path
from loguru import logger

from .config import LOGS_DIR


def setup_logger(level: str = "INFO") -> None:
    """Configure the global logger."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Remove default handler
    logger.remove()

    # Console handler with colors
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[agent]:>12}</cyan> | "
            "<level>{message}</level>"
        ),
        level=level,
        colorize=True,
        filter=lambda record: "agent" in record["extra"],
    )

    # Fallback for non-agent logs
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{'SYSTEM':>12}</cyan> | "
            "<level>{message}</level>"
        ),
        level=level,
        colorize=True,
        filter=lambda record: "agent" not in record["extra"],
    )

    # File handler - all logs
    logger.add(
        LOGS_DIR / "system.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
    )

    # File handler - agent logs (all agents in one file)
    agents_dir = LOGS_DIR / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    logger.add(
        LOGS_DIR / "agents" / "all_agents.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[agent]:>12} | {message}",
        level="DEBUG",
        rotation="5 MB",
        retention="3 days",
        filter=lambda record: "agent" in record["extra"],
    )


def get_agent_logger(agent_name: str):
    """Get a logger bound to a specific agent."""
    return logger.bind(agent=agent_name)

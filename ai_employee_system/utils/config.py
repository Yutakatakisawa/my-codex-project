"""
Configuration management for AI Employee System.
"""
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

# Load .env file
load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent
MINDSETS_DIR = PROJECT_ROOT / "ai_employee_system" / "mindsets"
LOGS_DIR = PROJECT_ROOT / "logs"
OUTPUT_DIR = PROJECT_ROOT / "output"


@dataclass
class AnthropicConfig:
    api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    model_opus: str = "claude-sonnet-4-20250514"  # Jarvis (CSO) - top-tier reasoning
    model_sonnet: str = "claude-sonnet-4-20250514"  # Max (Engineer)
    model_haiku: str = "claude-sonnet-4-20250514"  # Sam (Content)
    max_tokens: int = 8192


@dataclass
class GeminiConfig:
    api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))
    model_pro: str = "gemini-2.0-flash"  # Pixel (Designer)
    model_flash: str = "gemini-2.0-flash"  # Riley (Customer Success)


@dataclass
class GLMConfig:
    api_key: str = field(default_factory=lambda: os.getenv("GLM_API_KEY", ""))
    base_url: str = field(default_factory=lambda: os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4"))
    model: str = "glm-4"  # Alice (Research), Quinn (Analytics)


@dataclass
class OpenAIConfig:
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = "gpt-4o"  # Nova (Marketing)
    base_url: str = "https://api.openai.com/v1"


@dataclass
class TelegramConfig:
    bot_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    chat_id: str = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID", ""))
    enabled: bool = field(default_factory=lambda: bool(os.getenv("TELEGRAM_BOT_TOKEN", "")))


@dataclass
class FirecrawlConfig:
    api_key: str = field(default_factory=lambda: os.getenv("FIRECRAWL_API_KEY", ""))


@dataclass
class DashboardConfig:
    host: str = field(default_factory=lambda: os.getenv("DASHBOARD_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("DASHBOARD_PORT", "8080")))


@dataclass
class SystemConfig:
    """Master configuration for the entire system."""
    anthropic: AnthropicConfig = field(default_factory=AnthropicConfig)
    gemini: GeminiConfig = field(default_factory=GeminiConfig)
    glm: GLMConfig = field(default_factory=GLMConfig)
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    firecrawl: FirecrawlConfig = field(default_factory=FirecrawlConfig)
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    max_concurrent_agents: int = field(default_factory=lambda: int(os.getenv("MAX_CONCURRENT_AGENTS", "7")))
    heartbeat_interval: int = field(default_factory=lambda: int(os.getenv("AGENT_HEARTBEAT_INTERVAL", "30")))


def get_config() -> SystemConfig:
    """Get system configuration singleton."""
    return SystemConfig()

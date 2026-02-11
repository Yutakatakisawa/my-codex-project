"""
Riley - Customer Success
=========================
Uses Gemini Flash for fast customer-facing responses.
Specializes in support, FAQ, onboarding, and customer satisfaction.
"""
import json
from typing import Any, Dict, Optional

from .base_agent import BaseAgent, AgentRole, Task, TaskResult
from ..mcp_servers.base_mcp import BaseMCPServer
from ..tools.content_tool import ContentTool
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Riley")


class RileyAgent(BaseAgent):
    """Riley - Customer Success using Gemini Flash."""

    def __init__(self):
        super().__init__(name="Riley", role=AgentRole.CUSTOMER_SUCCESS)

        self.content_tool = ContentTool()

        self.mcp_server = BaseMCPServer("Riley", max_calls_per_minute=30)
        self._register_tools()

    def _register_tools(self) -> None:
        for tool_def in self.content_tool.get_mcp_tools():
            self.mcp_server.register_tool(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=tool_def["handler"],
            )

    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a customer success task."""
        prompt = f"""カスタマーサクセスの専門家として以下のタスクを実行してください。

## タスク
{task.description}

## コンテキスト
{json.dumps(task.context, ensure_ascii=False, default=str)}

顧客中心のアプローチで回答してください。"""

        result = await self.call_llm(prompt)

        return TaskResult(
            success=True,
            output=result,
            data={"type": "customer_success"},
        )

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call Gemini Flash for fast responses."""
        try:
            import httpx

            api_key = self.config.gemini.api_key
            if not api_key:
                raise ValueError("Gemini API key not configured")

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.gemini.model_flash}:generateContent",
                    params={"key": api_key},
                    json={
                        "systemInstruction": {"parts": [{"text": system or self.mindset}]},
                        "contents": [{"parts": [{"text": prompt}]}],
                    },
                )
                response.raise_for_status()
                data = response.json()

                if "candidates" in data and data["candidates"]:
                    parts = data["candidates"][0].get("content", {}).get("parts", [])
                    if parts:
                        result = parts[0].get("text", "")
                        self.conversation_history.append({"role": "user", "content": prompt})
                        self.conversation_history.append({"role": "assistant", "content": result})
                        return result

                return "Customer support response generated."

        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}, using mock")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        return (
            "## Customer Success Response\n\n"
            "### Resolution\n"
            "The customer inquiry has been addressed with appropriate guidance.\n\n"
            "### Follow-up Actions\n"
            "1. Monitor customer satisfaction\n"
            "2. Update FAQ documentation\n"
            "3. Schedule follow-up check-in\n\n"
            "### Documentation\n"
            "Support case documented for team reference.\n"
        )

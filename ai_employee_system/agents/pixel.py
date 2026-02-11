"""
Pixel - Product Designer
=========================
Uses Gemini Pro API for design reasoning + image generation tools.
Specializes in UI/UX, marketing visuals, and branding.
"""
import json
from typing import Any, Dict, Optional

from .base_agent import BaseAgent, AgentRole, Task, TaskResult
from ..mcp_servers.base_mcp import BaseMCPServer
from ..tools.image_gen_tool import ImageGenTool
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Pixel")


class PixelAgent(BaseAgent):
    """Pixel - Product Designer using Gemini + Image Generation."""

    def __init__(self):
        super().__init__(name="Pixel", role=AgentRole.PRODUCT_DESIGNER)

        # Initialize tools
        self.image_gen = ImageGenTool()

        # Setup MCP server
        self.mcp_server = BaseMCPServer("Pixel", max_calls_per_minute=15)
        self._register_tools()

    def _register_tools(self) -> None:
        """Register design tools on Pixel's MCP server."""
        for tool_def in self.image_gen.get_mcp_tools():
            self.mcp_server.register_tool(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=tool_def["handler"],
            )

    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a design task."""
        description = task.description.lower()
        tool_results = []

        if any(word in description for word in ["marketing", "マーケティング", "広告", "ad"]):
            result = await self.mcp_server.call_tool(
                "generate_marketing_image",
                {
                    "product_name": task.context.get("product_name", "Product"),
                    "description": task.description,
                    "target_audience": task.context.get("target_audience", "general"),
                },
            )
            tool_results.append(("marketing_image", result))

        elif any(word in description for word in ["ui", "ux", "mockup", "モックアップ", "画面"]):
            result = await self.mcp_server.call_tool(
                "generate_ui_mockup",
                {
                    "app_name": task.context.get("app_name", "App"),
                    "screen_description": task.description,
                    "platform": task.context.get("platform", "web"),
                },
            )
            tool_results.append(("ui_mockup", result))

        else:
            result = await self.mcp_server.call_tool(
                "generate_image",
                {
                    "prompt": task.description,
                    "style": task.context.get("style", "professional"),
                },
            )
            tool_results.append(("image", result))

        # Analyze results with LLM
        tool_context = json.dumps(tool_results, ensure_ascii=False, default=str)[:2000]

        prompt = f"""デザインタスクの結果をレビューし、最終的なデザイン提案をまとめてください。

## タスク
{task.description}

## 生成結果
{tool_context}

デザインの説明、カラーパレット、レイアウト提案を含めてください。"""

        analysis = await self.call_llm(prompt)

        return TaskResult(
            success=True,
            output=analysis,
            data={
                "tool_calls": len(tool_results),
                "design_assets": [name for name, _ in tool_results],
            },
        )

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call Gemini Pro for Pixel's reasoning."""
        try:
            import httpx

            api_key = self.config.gemini.api_key
            if not api_key:
                raise ValueError("Gemini API key not configured")

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.gemini.model_pro}:generateContent",
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

                return "Design analysis completed."

        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}, using mock")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        """Mock response for testing."""
        return (
            "## Design Proposal\n\n"
            "### Visual Concept\n"
            "Modern, clean design with a focus on usability.\n\n"
            "### Color Palette\n"
            "- Primary: #2563EB (Blue)\n"
            "- Secondary: #7C3AED (Purple)\n"
            "- Background: #F8FAFC\n"
            "- Text: #1E293B\n\n"
            "### Layout\n"
            "Responsive grid layout with clear visual hierarchy.\n\n"
            "### Typography\n"
            "- Headings: Inter Bold\n"
            "- Body: Inter Regular\n"
        )

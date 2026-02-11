"""
Sam - Content Creator
======================
Uses Claude Haiku for fast content generation.
Specializes in blog posts, social media, copywriting, and email marketing.
"""
import json
from typing import Any, Dict, Optional

from .base_agent import BaseAgent, AgentRole, Task, TaskResult
from ..mcp_servers.base_mcp import BaseMCPServer
from ..tools.content_tool import ContentTool
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Sam")


class SamAgent(BaseAgent):
    """Sam - Content Creator using Claude Haiku."""

    def __init__(self):
        super().__init__(name="Sam", role=AgentRole.CONTENT_CREATOR)

        self.content_tool = ContentTool()

        self.mcp_server = BaseMCPServer("Sam", max_calls_per_minute=30)
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
        """Execute a content creation task."""
        description = task.description.lower()

        prompt = f"""コンテンツクリエイターとして以下のタスクを実行してください。

## タスク
{task.description}

## コンテキスト
{json.dumps(task.context, ensure_ascii=False, default=str)}

魅力的で読者を引きつけるコンテンツを作成してください。"""

        content = await self.call_llm(prompt)

        # Save content using tools
        if any(word in description for word in ["blog", "ブログ", "記事"]):
            await self.mcp_server.call_tool(
                "write_content",
                {
                    "title": task.description[:50],
                    "content": content,
                    "content_type": "blog",
                },
            )
        elif any(word in description for word in ["social", "sns", "twitter", "投稿"]):
            await self.mcp_server.call_tool(
                "create_social_post",
                {
                    "platform": task.context.get("platform", "twitter"),
                    "message": content[:280],
                },
            )
        elif any(word in description for word in ["email", "メール"]):
            await self.mcp_server.call_tool(
                "create_email_template",
                {
                    "subject": task.description[:50],
                    "body": content,
                    "email_type": task.context.get("email_type", "marketing"),
                },
            )

        return TaskResult(
            success=True,
            output=content,
            data={"type": "content_creation"},
        )

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call Claude Haiku for fast content generation."""
        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=self.config.anthropic.api_key)

            messages = []
            for msg in self.conversation_history[-6:]:
                messages.append(msg)
            messages.append({"role": "user", "content": prompt})

            response = await client.messages.create(
                model=self.config.anthropic.model_haiku,
                max_tokens=4096,
                system=system or self.mindset,
                messages=messages,
            )

            result = response.content[0].text

            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": result})

            if response.usage:
                self.total_tokens_used += response.usage.input_tokens + response.usage.output_tokens

            return result

        except Exception as e:
            logger.warning(f"Claude API call failed: {e}, using mock")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        return (
            "## Content Draft\n\n"
            "### Title: Building the Future with AI\n\n"
            "In today's rapidly evolving technological landscape, "
            "artificial intelligence is reshaping how businesses operate. "
            "From automated workflows to intelligent decision-making, "
            "the possibilities are endless.\n\n"
            "### Key Takeaways\n"
            "1. AI automation reduces costs by up to 70%\n"
            "2. 24/7 operations without human fatigue\n"
            "3. Scalable solutions for growing businesses\n\n"
            "*Ready to transform your business? Let's get started.*\n"
        )

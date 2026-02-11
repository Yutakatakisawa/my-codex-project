"""
Nova - Marketing Strategist
=============================
Uses GPT-4o for marketing strategy and campaign planning.
"""
import json
from typing import Any, Dict, Optional

from .base_agent import BaseAgent, AgentRole, Task, TaskResult
from ..mcp_servers.base_mcp import BaseMCPServer
from ..tools.web_search_tool import WebSearchTool
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Nova")


class NovaAgent(BaseAgent):
    """Nova - Marketing Strategist using GPT-4o."""

    def __init__(self):
        super().__init__(name="Nova", role=AgentRole.MARKETING_STRATEGIST)

        self.web_search = WebSearchTool()

        self.mcp_server = BaseMCPServer("Nova", max_calls_per_minute=20)
        self._register_tools()

    def _register_tools(self) -> None:
        for tool_def in self.web_search.get_mcp_tools():
            self.mcp_server.register_tool(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=tool_def["handler"],
            )

    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a marketing task."""
        prompt = f"""マーケティング戦略の専門家として以下のタスクを実行してください。

## タスク
{task.description}

## コンテキスト
{json.dumps(task.context, ensure_ascii=False, default=str)}

以下の観点で戦略を立案してください：
1. ターゲット市場分析
2. 競合ポジショニング
3. チャネル戦略
4. KPI設定
5. アクションプラン"""

        result = await self.call_llm(prompt)

        return TaskResult(
            success=True,
            output=result,
            data={"type": "marketing_strategy"},
        )

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call GPT-4o for Nova's marketing reasoning."""
        try:
            import openai

            client = openai.AsyncOpenAI(
                api_key=self.config.openai.api_key,
                base_url=self.config.openai.base_url,
            )

            messages = [
                {"role": "system", "content": system or self.mindset},
            ]
            for msg in self.conversation_history[-6:]:
                messages.append(msg)
            messages.append({"role": "user", "content": prompt})

            response = await client.chat.completions.create(
                model=self.config.openai.model,
                messages=messages,
                max_tokens=4096,
            )

            result = response.choices[0].message.content

            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": result})

            if response.usage:
                self.total_tokens_used += response.usage.total_tokens

            return result

        except Exception as e:
            logger.warning(f"OpenAI API call failed: {e}, using mock")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        return (
            "## Marketing Strategy\n\n"
            "### Target Market\n"
            "Tech-savvy professionals aged 25-45 seeking AI-powered solutions.\n\n"
            "### Positioning\n"
            "Premium AI automation platform for forward-thinking businesses.\n\n"
            "### Channel Strategy\n"
            "1. LinkedIn: Thought leadership & B2B\n"
            "2. Twitter/X: Community engagement\n"
            "3. Content Marketing: SEO-driven blog\n\n"
            "### KPIs\n"
            "- MQL growth: 30% MoM\n"
            "- CAC: < $50\n"
            "- LTV/CAC: > 3x\n\n"
            "### Action Plan\n"
            "Week 1-2: Content foundation\n"
            "Week 3-4: Campaign launch\n"
        )

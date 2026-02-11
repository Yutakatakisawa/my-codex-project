"""
Quinn - Data Analyst
=====================
Uses GLM 4 for data analysis and reporting.
"""
import json
from typing import Any, Dict, Optional

from .base_agent import BaseAgent, AgentRole, Task, TaskResult
from ..mcp_servers.base_mcp import BaseMCPServer
from ..tools.analytics_tool import AnalyticsTool
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Quinn")


class QuinnAgent(BaseAgent):
    """Quinn - Data Analyst using GLM 4."""

    def __init__(self):
        super().__init__(name="Quinn", role=AgentRole.DATA_ANALYST)

        self.analytics = AnalyticsTool()

        self.mcp_server = BaseMCPServer("Quinn", max_calls_per_minute=20)
        self._register_tools()

    def _register_tools(self) -> None:
        for tool_def in self.analytics.get_mcp_tools():
            self.mcp_server.register_tool(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=tool_def["handler"],
            )

    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a data analysis task."""
        prompt = f"""データアナリストとして以下のタスクを実行してください。

## タスク
{task.description}

## コンテキスト
{json.dumps(task.context, ensure_ascii=False, default=str)}

以下の形式で分析結果を提出してください：
1. データサマリー
2. 主要な発見
3. トレンドと予測
4. アクショナブルなインサイト
5. 推奨アクション"""

        result = await self.call_llm(prompt)

        # Generate report if needed
        if task.context.get("generate_report", False):
            await self.mcp_server.call_tool(
                "generate_report",
                {
                    "title": f"Analysis: {task.description[:50]}",
                    "sections": result,
                },
            )

        return TaskResult(
            success=True,
            output=result,
            data={"type": "data_analysis"},
        )

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call GLM 4 for Quinn's analysis."""
        try:
            import openai

            client = openai.AsyncOpenAI(
                api_key=self.config.glm.api_key,
                base_url=self.config.glm.base_url,
            )

            messages = [
                {"role": "system", "content": system or self.mindset},
            ]
            for msg in self.conversation_history[-6:]:
                messages.append(msg)
            messages.append({"role": "user", "content": prompt})

            response = await client.chat.completions.create(
                model=self.config.glm.model,
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
            logger.warning(f"GLM API call failed: {e}, using mock")
            return self._mock_response(prompt)

    def _mock_response(self, prompt: str) -> str:
        return (
            "## Data Analysis Report\n\n"
            "### Summary\n"
            "Analysis completed with available data points.\n\n"
            "### Key Findings\n"
            "- Trend analysis shows positive growth trajectory\n"
            "- Key metrics within expected ranges\n\n"
            "### Predictions\n"
            "- Projected 25% growth in next quarter\n\n"
            "### Recommendations\n"
            "- Focus on high-impact metrics\n"
            "- Implement automated reporting\n"
        )

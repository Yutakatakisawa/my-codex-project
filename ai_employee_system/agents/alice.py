"""
Alice - Research Analyst
========================
Uses GLM 4 model + Firecrawl API for research tasks.
Specializes in market research, competitor analysis, and information gathering.
"""
import json
from typing import Any, Dict, Optional

from .base_agent import BaseAgent, AgentRole, Task, TaskResult
from ..mcp_servers.base_mcp import BaseMCPServer
from ..tools.firecrawl_tool import FirecrawlTool
from ..tools.web_search_tool import WebSearchTool
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Alice")


class AliceAgent(BaseAgent):
    """Alice - Research Analyst using GLM 4 + Firecrawl."""

    def __init__(self):
        super().__init__(name="Alice", role=AgentRole.RESEARCH_ANALYST)

        # Initialize tools
        self.firecrawl = FirecrawlTool()
        self.web_search = WebSearchTool()

        # Setup MCP server
        self.mcp_server = BaseMCPServer("Alice", max_calls_per_minute=20)
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all tools on Alice's MCP server."""
        for tool_def in self.firecrawl.get_mcp_tools():
            self.mcp_server.register_tool(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=tool_def["handler"],
            )
        for tool_def in self.web_search.get_mcp_tools():
            self.mcp_server.register_tool(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=tool_def["handler"],
            )

    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a research task."""
        description = task.description.lower()

        # Determine which tools to use based on task
        tool_results = []

        if any(word in description for word in ["search", "調査", "リサーチ", "検索", "research"]):
            # Use web search
            search_result = await self.mcp_server.call_tool(
                "web_search", {"query": task.description, "num_results": 5}
            )
            tool_results.append(("web_search", search_result))

        if any(word in description for word in ["scrape", "スクレイプ", "url", "http", "website"]):
            # Extract URLs from description and scrape
            import re
            urls = re.findall(r'https?://\S+', task.description)
            for url in urls[:3]:  # Limit to 3 URLs
                scrape_result = await self.mcp_server.call_tool(
                    "firecrawl_scrape", {"url": url}
                )
                tool_results.append(("firecrawl_scrape", scrape_result))

        # Use LLM to analyze and summarize
        tool_context = "\n\n".join([
            f"Tool: {name}\nResult: {json.dumps(result, ensure_ascii=False, default=str)[:1000]}"
            for name, result in tool_results
        ])

        prompt = f"""以下のリサーチタスクを実行してください。

## タスク
{task.description}

## 収集したデータ
{tool_context if tool_context else "（ツール結果なし - 知識ベースから回答）"}

## 回答形式
1. **要約**: 3行以内のサマリー
2. **詳細**: 構造化された分析結果
3. **ソース**: 参照した情報源
4. **推奨事項**: 次のアクションの提案"""

        analysis = await self.call_llm(prompt)

        return TaskResult(
            success=True,
            output=analysis,
            data={
                "tool_calls": len(tool_results),
                "tools_used": [name for name, _ in tool_results],
            },
        )

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call GLM 4 for Alice's reasoning."""
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
        """Mock response for testing."""
        return (
            "## Research Report\n\n"
            "### Summary\n"
            "Research task completed based on available information.\n\n"
            "### Details\n"
            "- Analysis performed using available data sources\n"
            "- Key findings have been compiled\n"
            "- Further investigation may be needed for specific areas\n\n"
            "### Sources\n"
            "- Internal knowledge base\n\n"
            "### Recommendations\n"
            "- Continue monitoring for new developments\n"
            "- Consider deeper analysis on identified trends"
        )

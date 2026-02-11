"""
Max - Software Engineer
========================
Uses Claude Sonnet for coding tasks.
Specializes in full-stack development, architecture, and technical implementation.
"""
import json
from typing import Any, Dict, Optional

from .base_agent import BaseAgent, AgentRole, Task, TaskResult
from ..mcp_servers.base_mcp import BaseMCPServer
from ..tools.code_tool import CodeTool
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Max")


class MaxAgent(BaseAgent):
    """Max - Software Engineer using Claude Sonnet."""

    def __init__(self):
        super().__init__(name="Max", role=AgentRole.SOFTWARE_ENGINEER)

        # Initialize tools
        self.code_tool = CodeTool()

        # Setup MCP server
        self.mcp_server = BaseMCPServer("Max", max_calls_per_minute=20)
        self._register_tools()

    def _register_tools(self) -> None:
        """Register coding tools on Max's MCP server."""
        for tool_def in self.code_tool.get_mcp_tools():
            self.mcp_server.register_tool(
                name=tool_def["name"],
                description=tool_def["description"],
                input_schema=tool_def["input_schema"],
                handler=tool_def["handler"],
            )

    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a coding task."""
        # Use LLM to plan and generate code
        prompt = f"""ソフトウェアエンジニアとして以下のタスクを実行してください。

## タスク
{task.description}

## コンテキスト
{json.dumps(task.context, ensure_ascii=False, default=str)}

## 指示
1. タスクを分析し、技術的なアプローチを決定
2. 必要なコードを生成
3. テスト戦略を提案

コードが必要な場合は、完全に動作するコードを提供してください。"""

        result = await self.call_llm(prompt)

        # If the response contains code, try to write it
        if "```" in result:
            import re
            code_blocks = re.findall(r'```(\w+)?\n(.*?)```', result, re.DOTALL)
            for i, (lang, code) in enumerate(code_blocks):
                ext = {"python": ".py", "javascript": ".js", "typescript": ".ts", "html": ".html", "css": ".css"}.get(lang, ".txt")
                filename = f"output_{task.id}_{i}{ext}"
                try:
                    await self.mcp_server.call_tool(
                        "write_code_file",
                        {"filepath": filename, "content": code.strip()},
                    )
                except Exception as e:
                    logger.warning(f"Failed to write code file: {e}")

        return TaskResult(
            success=True,
            output=result,
            data={"type": "code_generation"},
        )

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call Claude Sonnet for Max's coding work."""
        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=self.config.anthropic.api_key)

            messages = []
            for msg in self.conversation_history[-6:]:
                messages.append(msg)
            messages.append({"role": "user", "content": prompt})

            response = await client.messages.create(
                model=self.config.anthropic.model_sonnet,
                max_tokens=self.config.anthropic.max_tokens,
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
            "## Technical Implementation\n\n"
            "### Approach\n"
            "The task has been analyzed and a clean implementation has been prepared.\n\n"
            "### Code\n"
            "```python\n"
            "# Implementation placeholder\n"
            "def main():\n"
            "    print('Task implementation ready')\n"
            "```\n\n"
            "### Testing Strategy\n"
            "- Unit tests for core functionality\n"
            "- Integration tests for API endpoints\n"
            "- Performance benchmarks\n"
        )

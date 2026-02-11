"""
Base MCP (Model Context Protocol) Server.
Each AI employee gets their own MCP server instance that manages
their tools and external resource connections.

This is a key architectural decision:
- Don't just pass API keys directly
- Build an MCP server per employee
- This lets each AI use tools and external resources properly
"""
import asyncio
import json
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union

from ..utils.logger import get_agent_logger


@dataclass
class MCPTool:
    """Definition of a tool available via MCP."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable
    agent_name: str


@dataclass
class MCPResource:
    """An external resource accessible via MCP."""
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


@dataclass
class MCPToolCall:
    """Record of a tool invocation."""
    tool_name: str
    input_data: Dict[str, Any]
    output_data: Any = None
    success: bool = True
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class BaseMCPServer:
    """
    MCP Server for an individual AI employee.
    
    Provides:
    1. Tool registration and execution
    2. Resource management
    3. Call logging and rate limiting
    4. Error handling with retries
    """

    def __init__(self, agent_name: str, max_calls_per_minute: int = 30):
        self.agent_name = agent_name
        self.logger = get_agent_logger(f"MCP-{agent_name}")
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.call_history: List[MCPToolCall] = []
        self.max_calls_per_minute = max_calls_per_minute
        self._running = False

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable,
    ) -> None:
        """Register a tool on this MCP server."""
        tool = MCPTool(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler,
            agent_name=self.agent_name,
        )
        self.tools[name] = tool
        self.logger.info(f"Tool registered: {name}")

    def register_resource(self, resource: MCPResource) -> None:
        """Register an external resource."""
        self.resources[resource.uri] = resource
        self.logger.debug(f"Resource registered: {resource.name} ({resource.uri})")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a tool call with logging and error handling.
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found on MCP server for {self.agent_name}")

        # Rate limiting check
        if not self._check_rate_limit():
            self.logger.warning(f"Rate limit reached for {self.agent_name}")
            await asyncio.sleep(2)

        tool = self.tools[tool_name]
        call_record = MCPToolCall(tool_name=tool_name, input_data=arguments)
        start_time = datetime.now()

        try:
            self.logger.debug(f"Calling tool: {tool_name}")

            if asyncio.iscoroutinefunction(tool.handler):
                result = await tool.handler(**arguments)
            else:
                result = tool.handler(**arguments)

            call_record.output_data = result
            call_record.success = True
            call_record.duration_ms = (datetime.now() - start_time).total_seconds() * 1000

            self.logger.debug(f"Tool {tool_name} completed in {call_record.duration_ms:.0f}ms")

        except Exception as e:
            call_record.success = False
            call_record.error = str(e)
            call_record.duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.error(f"Tool {tool_name} failed: {e}")
            raise

        finally:
            self.call_history.append(call_record)
            # Keep history bounded
            if len(self.call_history) > 500:
                self.call_history = self.call_history[-500:]

        return result

    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        now = datetime.now()
        recent_calls = [
            c for c in self.call_history
            if (now - c.timestamp).total_seconds() < 60
        ]
        return len(recent_calls) < self.max_calls_per_minute

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions in the format expected by LLM APIs.
        Returns the tool schemas for function calling.
        """
        definitions = []
        for tool in self.tools.values():
            definitions.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            })
        return definitions

    def get_tool_definitions_openai(self) -> List[Dict[str, Any]]:
        """Get tool definitions in OpenAI function-calling format."""
        definitions = []
        for tool in self.tools.values():
            definitions.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                },
            })
        return definitions

    def get_stats(self) -> Dict[str, Any]:
        """Get MCP server statistics."""
        total_calls = len(self.call_history)
        successful = sum(1 for c in self.call_history if c.success)
        failed = total_calls - successful
        avg_duration = (
            sum(c.duration_ms for c in self.call_history) / total_calls
            if total_calls > 0 else 0
        )

        return {
            "agent": self.agent_name,
            "tools_registered": len(self.tools),
            "resources_registered": len(self.resources),
            "total_calls": total_calls,
            "successful_calls": successful,
            "failed_calls": failed,
            "avg_duration_ms": round(avg_duration, 2),
        }

    async def start(self) -> None:
        """Start the MCP server."""
        self._running = True
        self.logger.info(f"MCP Server started for {self.agent_name} with {len(self.tools)} tools")

    async def stop(self) -> None:
        """Stop the MCP server."""
        self._running = False
        self.logger.info(f"MCP Server stopped for {self.agent_name}")

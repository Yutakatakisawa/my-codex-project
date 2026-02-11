"""
Global tool registry - manages all MCP servers and their tools.
Acts as the central hub connecting Jarvis to all employee MCP servers.
"""
from typing import Any, Dict, List, Optional

from .base_mcp import BaseMCPServer
from ..utils.logger import get_agent_logger

logger = get_agent_logger("ToolRegistry")


class ToolRegistry:
    """
    Central registry of all MCP servers and their tools.
    Jarvis uses this to know what each employee can do.
    """

    def __init__(self):
        self._servers: Dict[str, BaseMCPServer] = {}

    def register_server(self, agent_name: str, server: BaseMCPServer) -> None:
        """Register an agent's MCP server."""
        self._servers[agent_name] = server
        logger.info(f"Registered MCP server for {agent_name}")

    def get_server(self, agent_name: str) -> Optional[BaseMCPServer]:
        """Get an agent's MCP server."""
        return self._servers.get(agent_name)

    def get_all_capabilities(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get a summary of all agent capabilities.
        Used by Jarvis to decide who to delegate to.
        """
        capabilities = {}
        for agent_name, server in self._servers.items():
            capabilities[agent_name] = server.get_tool_definitions()
        return capabilities

    def get_capability_summary(self) -> str:
        """
        Get a human-readable summary of all capabilities.
        This is injected into Jarvis's context.
        """
        lines = ["## Available AI Employees and Their Capabilities\n"]
        for agent_name, server in self._servers.items():
            lines.append(f"### {agent_name}")
            for tool in server.tools.values():
                lines.append(f"  - **{tool.name}**: {tool.description}")
            lines.append("")
        return "\n".join(lines)

    async def call_agent_tool(
        self,
        agent_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> Any:
        """Call a tool on a specific agent's MCP server."""
        server = self._servers.get(agent_name)
        if not server:
            raise ValueError(f"No MCP server found for agent: {agent_name}")
        return await server.call_tool(tool_name, arguments)

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get stats from all MCP servers."""
        return {name: server.get_stats() for name, server in self._servers.items()}


# Global registry singleton
tool_registry = ToolRegistry()

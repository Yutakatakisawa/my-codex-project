"""
Web Search Tool - For Nova (Marketing) and general research.
"""
import asyncio
from typing import Any, Dict, List, Optional

import httpx

from ..utils.logger import get_agent_logger

logger = get_agent_logger("WebSearchTool")


class WebSearchTool:
    """Web search capabilities for agents."""

    async def search_web(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Args:
            query: Search query
            num_results: Number of results to return
        """
        # Uses DuckDuckGo HTML as a free fallback
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(
                    "https://html.duckduckgo.com/html/",
                    params={"q": query},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                # Parse basic results from HTML
                text = response.text
                results = []
                # Extract result snippets
                import re
                snippets = re.findall(r'class="result__snippet">(.*?)</a>', text, re.DOTALL)
                titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', text, re.DOTALL)
                urls = re.findall(r'class="result__url"[^>]*>(.*?)</a>', text, re.DOTALL)
                
                for i in range(min(num_results, len(snippets))):
                    results.append({
                        "title": titles[i].strip() if i < len(titles) else "",
                        "url": urls[i].strip() if i < len(urls) else "",
                        "snippet": snippets[i].strip() if i < len(snippets) else "",
                    })

                logger.info(f"Web search: '{query}' -> {len(results)} results")
                return {"success": True, "results": results, "query": query}

        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return {"success": False, "error": str(e), "query": query}

    async def fetch_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from a URL.
        
        Args:
            url: URL to fetch
        """
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                return {
                    "success": True,
                    "url": url,
                    "status_code": response.status_code,
                    "content": response.text[:5000],  # Limit content size
                }
        except Exception as e:
            return {"success": False, "error": str(e), "url": url}

    def get_mcp_tools(self) -> list:
        """Return MCP tool definitions."""
        return [
            {
                "name": "web_search",
                "description": "Search the web for information",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "num_results": {"type": "integer", "description": "Number of results", "default": 5},
                    },
                    "required": ["query"],
                },
                "handler": self.search_web,
            },
            {
                "name": "fetch_url",
                "description": "Fetch content from a URL",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to fetch"},
                    },
                    "required": ["url"],
                },
                "handler": self.fetch_url,
            },
        ]

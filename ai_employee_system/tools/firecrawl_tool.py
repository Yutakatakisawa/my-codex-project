"""
Firecrawl Tool - Web scraping and research tool for Alice.
Uses the Firecrawl API to crawl, scrape, and extract data from websites.
"""
import asyncio
from typing import Any, Dict, Optional

import httpx

from ..utils.config import get_config
from ..utils.logger import get_agent_logger

logger = get_agent_logger("FirecrawlTool")


class FirecrawlTool:
    """Web scraping and research tool using Firecrawl API."""

    BASE_URL = "https://api.firecrawl.dev/v1"

    def __init__(self):
        config = get_config()
        self.api_key = config.firecrawl.api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def scrape_url(self, url: str, formats: Optional[list] = None) -> Dict[str, Any]:
        """
        Scrape a single URL and extract its content.
        
        Args:
            url: The URL to scrape
            formats: Output formats (e.g., ["markdown", "html"])
        """
        if not self.api_key:
            return {"success": False, "error": "Firecrawl API key not configured"}

        payload = {"url": url}
        if formats:
            payload["formats"] = formats
        else:
            payload["formats"] = ["markdown"]

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.BASE_URL}/scrape",
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Scraped URL: {url}")
                return {"success": True, "data": data}
        except Exception as e:
            logger.error(f"Scrape failed for {url}: {e}")
            return {"success": False, "error": str(e)}

    async def crawl_site(self, url: str, max_pages: int = 10) -> Dict[str, Any]:
        """
        Crawl an entire website starting from a URL.
        
        Args:
            url: Starting URL
            max_pages: Maximum number of pages to crawl
        """
        if not self.api_key:
            return {"success": False, "error": "Firecrawl API key not configured"}

        payload = {
            "url": url,
            "limit": max_pages,
            "scrapeOptions": {"formats": ["markdown"]},
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.BASE_URL}/crawl",
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Crawl initiated for: {url}")
                return {"success": True, "data": data}
        except Exception as e:
            logger.error(f"Crawl failed for {url}: {e}")
            return {"success": False, "error": str(e)}

    async def search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search the web and get scraped results.
        
        Args:
            query: Search query
            limit: Number of results
        """
        if not self.api_key:
            return {"success": False, "error": "Firecrawl API key not configured"}

        payload = {
            "query": query,
            "limit": limit,
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.BASE_URL}/search",
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Search completed for: {query}")
                return {"success": True, "data": data}
        except Exception as e:
            logger.error(f"Search failed for {query}: {e}")
            return {"success": False, "error": str(e)}

    def get_mcp_tools(self) -> list:
        """Return MCP tool definitions for this tool."""
        return [
            {
                "name": "firecrawl_scrape",
                "description": "Scrape a single URL and extract its content as markdown",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to scrape"},
                    },
                    "required": ["url"],
                },
                "handler": self.scrape_url,
            },
            {
                "name": "firecrawl_crawl",
                "description": "Crawl an entire website starting from a URL",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "Starting URL"},
                        "max_pages": {"type": "integer", "description": "Max pages to crawl", "default": 10},
                    },
                    "required": ["url"],
                },
                "handler": self.crawl_site,
            },
            {
                "name": "firecrawl_search",
                "description": "Search the web and get scraped content from results",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "integer", "description": "Number of results", "default": 5},
                    },
                    "required": ["query"],
                },
                "handler": self.search,
            },
        ]

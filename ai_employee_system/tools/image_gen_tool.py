"""
Image Generation Tool - For Pixel (Product Designer).
Supports multiple image generation backends.
"""
import asyncio
import base64
import os
from pathlib import Path
from typing import Any, Dict, Optional

import httpx

from ..utils.config import get_config, OUTPUT_DIR
from ..utils.logger import get_agent_logger

logger = get_agent_logger("ImageGenTool")


class ImageGenTool:
    """Image generation tool using various APIs."""

    def __init__(self):
        self.config = get_config()
        self.output_dir = OUTPUT_DIR / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_with_gemini(
        self,
        prompt: str,
        style: str = "professional",
        size: str = "1024x1024",
    ) -> Dict[str, Any]:
        """
        Generate an image using Gemini's image capabilities.
        
        Args:
            prompt: Image description
            style: Style hint (professional, creative, minimal, etc.)
            size: Image dimensions
        """
        if not self.config.gemini.api_key:
            return {"success": False, "error": "Gemini API key not configured"}

        full_prompt = f"Create a {style} image: {prompt}. Size: {size}"

        try:
            # Use Gemini API for image description/concept
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.gemini.model_pro}:generateContent",
                    params={"key": self.config.gemini.api_key},
                    json={
                        "contents": [{"parts": [{"text": f"As a professional designer, create a detailed visual description and design specification for: {full_prompt}. Include color palette, layout, typography suggestions, and mood."}]}],
                    },
                )
                response.raise_for_status()
                data = response.json()
                
                design_spec = ""
                if "candidates" in data and data["candidates"]:
                    parts = data["candidates"][0].get("content", {}).get("parts", [])
                    if parts:
                        design_spec = parts[0].get("text", "")

                logger.info(f"Design spec generated for: {prompt[:50]}...")
                return {
                    "success": True,
                    "type": "design_spec",
                    "prompt": prompt,
                    "style": style,
                    "design_spec": design_spec,
                }

        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return {"success": False, "error": str(e)}

    async def generate_marketing_image(
        self,
        product_name: str,
        description: str,
        target_audience: str = "general",
    ) -> Dict[str, Any]:
        """
        Generate a marketing image concept.
        
        Args:
            product_name: Name of the product
            description: Product description
            target_audience: Target audience for the marketing
        """
        prompt = (
            f"Marketing image for '{product_name}': {description}. "
            f"Target audience: {target_audience}. "
            "Professional, clean, modern design suitable for social media and web."
        )
        return await self.generate_with_gemini(prompt, style="marketing")

    async def generate_ui_mockup(
        self,
        app_name: str,
        screen_description: str,
        platform: str = "web",
    ) -> Dict[str, Any]:
        """
        Generate a UI mockup description.
        
        Args:
            app_name: Application name
            screen_description: Description of the screen to design
            platform: Target platform (web, ios, android)
        """
        prompt = (
            f"UI mockup for '{app_name}' ({platform}): {screen_description}. "
            "Modern, clean interface following current design trends."
        )
        return await self.generate_with_gemini(prompt, style="ui-mockup")

    def get_mcp_tools(self) -> list:
        """Return MCP tool definitions."""
        return [
            {
                "name": "generate_image",
                "description": "Generate an image or design specification using AI",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Image description"},
                        "style": {"type": "string", "description": "Visual style", "default": "professional"},
                        "size": {"type": "string", "description": "Image size", "default": "1024x1024"},
                    },
                    "required": ["prompt"],
                },
                "handler": self.generate_with_gemini,
            },
            {
                "name": "generate_marketing_image",
                "description": "Generate a marketing image concept for a product",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product_name": {"type": "string", "description": "Product name"},
                        "description": {"type": "string", "description": "Product description"},
                        "target_audience": {"type": "string", "description": "Target audience", "default": "general"},
                    },
                    "required": ["product_name", "description"],
                },
                "handler": self.generate_marketing_image,
            },
            {
                "name": "generate_ui_mockup",
                "description": "Generate a UI mockup description for an application",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Application name"},
                        "screen_description": {"type": "string", "description": "Screen description"},
                        "platform": {"type": "string", "description": "Target platform", "default": "web"},
                    },
                    "required": ["app_name", "screen_description"],
                },
                "handler": self.generate_ui_mockup,
            },
        ]

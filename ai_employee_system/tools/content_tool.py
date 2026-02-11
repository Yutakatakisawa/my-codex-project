"""
Content Tool - For Sam (Content Creator).
Content creation and management capabilities.
"""
import asyncio
from pathlib import Path
from typing import Any, Dict, Optional

from ..utils.config import OUTPUT_DIR
from ..utils.logger import get_agent_logger

logger = get_agent_logger("ContentTool")


class ContentTool:
    """Content creation and management tool."""

    def __init__(self):
        self.output_dir = OUTPUT_DIR / "content"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def write_content(
        self,
        title: str,
        content: str,
        content_type: str = "blog",
    ) -> Dict[str, Any]:
        """
        Write content to a file.
        
        Args:
            title: Content title
            content: The content body
            content_type: Type (blog, social, email, landing_page)
        """
        try:
            filename = f"{content_type}_{title.replace(' ', '_').lower()}.md"
            filepath = self.output_dir / filename
            
            full_content = f"# {title}\n\n*Type: {content_type}*\n\n{content}"
            filepath.write_text(full_content, encoding="utf-8")
            
            logger.info(f"Content written: {filename}")
            return {
                "success": True,
                "path": str(filepath),
                "filename": filename,
                "word_count": len(content.split()),
            }
        except Exception as e:
            logger.error(f"Content write failed: {e}")
            return {"success": False, "error": str(e)}

    async def create_social_post(
        self,
        platform: str,
        message: str,
        hashtags: str = "",
    ) -> Dict[str, Any]:
        """
        Create a social media post.
        
        Args:
            platform: Target platform (twitter, linkedin, instagram)
            message: Post content
            hashtags: Relevant hashtags
        """
        try:
            char_limits = {
                "twitter": 280,
                "linkedin": 3000,
                "instagram": 2200,
            }
            limit = char_limits.get(platform, 2000)
            
            post = f"{message}\n\n{hashtags}" if hashtags else message
            
            if len(post) > limit:
                post = post[:limit-3] + "..."
            
            filename = f"social_{platform}_{asyncio.get_event_loop().time():.0f}.md"
            filepath = self.output_dir / filename
            filepath.write_text(post, encoding="utf-8")
            
            logger.info(f"Social post created for {platform}")
            return {
                "success": True,
                "platform": platform,
                "post": post,
                "char_count": len(post),
                "path": str(filepath),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_email_template(
        self,
        subject: str,
        body: str,
        email_type: str = "marketing",
    ) -> Dict[str, Any]:
        """
        Create an email template.
        
        Args:
            subject: Email subject line
            body: Email body content
            email_type: Type of email (marketing, onboarding, support)
        """
        try:
            template = f"Subject: {subject}\nType: {email_type}\n\n{body}"
            
            filename = f"email_{email_type}_{subject.replace(' ', '_').lower()[:30]}.md"
            filepath = self.output_dir / filename
            filepath.write_text(template, encoding="utf-8")
            
            logger.info(f"Email template created: {subject}")
            return {
                "success": True,
                "subject": subject,
                "path": str(filepath),
                "template": template,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_mcp_tools(self) -> list:
        """Return MCP tool definitions."""
        return [
            {
                "name": "write_content",
                "description": "Write blog posts, articles, or other content",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Content title"},
                        "content": {"type": "string", "description": "Content body"},
                        "content_type": {"type": "string", "description": "Content type", "default": "blog"},
                    },
                    "required": ["title", "content"],
                },
                "handler": self.write_content,
            },
            {
                "name": "create_social_post",
                "description": "Create a social media post for a specific platform",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "platform": {"type": "string", "description": "Platform (twitter, linkedin, instagram)"},
                        "message": {"type": "string", "description": "Post message"},
                        "hashtags": {"type": "string", "description": "Hashtags", "default": ""},
                    },
                    "required": ["platform", "message"],
                },
                "handler": self.create_social_post,
            },
            {
                "name": "create_email_template",
                "description": "Create an email template",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string", "description": "Email subject"},
                        "body": {"type": "string", "description": "Email body"},
                        "email_type": {"type": "string", "description": "Email type", "default": "marketing"},
                    },
                    "required": ["subject", "body"],
                },
                "handler": self.create_email_template,
            },
        ]

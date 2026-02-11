"""
Code Tool - For Max (Software Engineer).
Provides code generation, review, and execution capabilities.
"""
import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from ..utils.config import OUTPUT_DIR
from ..utils.logger import get_agent_logger

logger = get_agent_logger("CodeTool")


class CodeTool:
    """Code generation and execution tool."""

    def __init__(self):
        self.output_dir = OUTPUT_DIR / "code"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def write_file(self, filepath: str, content: str) -> Dict[str, Any]:
        """
        Write code to a file.
        
        Args:
            filepath: Relative path for the file
            content: File content
        """
        try:
            full_path = self.output_dir / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            logger.info(f"File written: {filepath}")
            return {"success": True, "path": str(full_path)}
        except Exception as e:
            logger.error(f"File write failed: {e}")
            return {"success": False, "error": str(e)}

    async def read_file(self, filepath: str) -> Dict[str, Any]:
        """
        Read a file's contents.
        
        Args:
            filepath: Path to the file
        """
        try:
            path = Path(filepath)
            if not path.exists():
                path = self.output_dir / filepath
            content = path.read_text(encoding="utf-8")
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def execute_python(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute Python code safely.
        
        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds
        """
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, dir=str(self.output_dir)
            ) as f:
                f.write(code)
                f.flush()
                
                process = await asyncio.create_subprocess_exec(
                    "python3", f.name,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(), timeout=timeout
                    )
                except asyncio.TimeoutError:
                    process.kill()
                    return {"success": False, "error": "Execution timed out"}

                return {
                    "success": process.returncode == 0,
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": stderr.decode("utf-8", errors="replace"),
                    "return_code": process.returncode,
                }
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return {"success": False, "error": str(e)}

    async def run_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Run a shell command.
        
        Args:
            command: Shell command to execute
            timeout: Timeout in seconds
        """
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.output_dir),
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                return {"success": False, "error": "Command timed out"}

            return {
                "success": process.returncode == 0,
                "stdout": stdout.decode("utf-8", errors="replace"),
                "stderr": stderr.decode("utf-8", errors="replace"),
                "return_code": process.returncode,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_mcp_tools(self) -> list:
        """Return MCP tool definitions."""
        return [
            {
                "name": "write_code_file",
                "description": "Write code to a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "File path (relative)"},
                        "content": {"type": "string", "description": "File content"},
                    },
                    "required": ["filepath", "content"],
                },
                "handler": self.write_file,
            },
            {
                "name": "read_code_file",
                "description": "Read a code file's contents",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "filepath": {"type": "string", "description": "File path"},
                    },
                    "required": ["filepath"],
                },
                "handler": self.read_file,
            },
            {
                "name": "execute_python",
                "description": "Execute Python code and return output",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Python code to execute"},
                        "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30},
                    },
                    "required": ["code"],
                },
                "handler": self.execute_python,
            },
            {
                "name": "run_shell_command",
                "description": "Run a shell command",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Shell command"},
                        "timeout": {"type": "integer", "description": "Timeout", "default": 30},
                    },
                    "required": ["command"],
                },
                "handler": self.run_command,
            },
        ]

"""
Jarvis - Chief Strategy Officer (CSO)
======================================
The main orchestrator agent. Uses Claude Opus for reasoning.

KEY DESIGN PRINCIPLE:
Jarvis does NOT do actual work. He THINKS and DELEGATES.
This saves tokens on the expensive Opus model and avoids API rate limits.

Jarvis:
1. Receives a task/objective
2. Analyzes and breaks it down
3. Delegates sub-tasks to specialized employees
4. Monitors progress and compiles results
5. Reports via Telegram
"""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent, AgentRole, AgentStatus, Task, TaskResult
from ..utils.config import get_config
from ..utils.events import Event, EventType, event_bus
from ..utils.logger import get_agent_logger
from ..mcp_servers.tool_registry import tool_registry

logger = get_agent_logger("Jarvis")


# Employee routing map
EMPLOYEE_CAPABILITIES = {
    "Alice": {
        "role": "Research Analyst",
        "skills": ["research", "web scraping", "market analysis", "competitor analysis", "data collection", "trend analysis"],
        "model": "GLM 4",
    },
    "Pixel": {
        "role": "Product Designer",
        "skills": ["ui design", "ux design", "image generation", "marketing visuals", "branding", "prototyping"],
        "model": "Gemini Pro",
    },
    "Max": {
        "role": "Software Engineer",
        "skills": ["coding", "architecture", "api development", "testing", "deployment", "debugging"],
        "model": "Claude Sonnet",
    },
    "Nova": {
        "role": "Marketing Strategist",
        "skills": ["marketing strategy", "campaigns", "seo", "advertising", "brand positioning", "growth"],
        "model": "GPT-4o",
    },
    "Quinn": {
        "role": "Data Analyst",
        "skills": ["data analysis", "metrics", "reporting", "dashboards", "statistics", "forecasting"],
        "model": "GLM 4",
    },
    "Riley": {
        "role": "Customer Success",
        "skills": ["customer support", "faq", "onboarding", "churn prevention", "feedback analysis"],
        "model": "Gemini Flash",
    },
    "Sam": {
        "role": "Content Creator",
        "skills": ["blog writing", "social media", "copywriting", "email marketing", "seo content"],
        "model": "Claude Haiku",
    },
}


class JarvisAgent(BaseAgent):
    """
    Jarvis - The CSO. Thinks and delegates, never does actual work.
    Uses Claude Opus for maximum reasoning capability.
    """

    def __init__(self):
        super().__init__(name="Jarvis", role=AgentRole.CSO)
        self.employees: Dict[str, BaseAgent] = {}
        self.delegation_results: Dict[str, TaskResult] = {}
        self._pending_delegations: Dict[str, asyncio.Event] = {}

        # Subscribe to task completion events
        self.event_bus.subscribe(EventType.TASK_COMPLETED, self._on_task_completed)
        self.event_bus.subscribe(EventType.TASK_FAILED, self._on_task_failed)

    def register_employee(self, agent: BaseAgent) -> None:
        """Register an AI employee under Jarvis's management."""
        self.employees[agent.name] = agent
        logger.info(f"Employee registered: {agent.name} ({agent.role.value})")

    async def execute_task(self, task: Task) -> TaskResult:
        """
        Jarvis's main task execution:
        1. Analyze the task
        2. Create a delegation plan
        3. Delegate to employees
        4. Compile results
        """
        self.status = AgentStatus.THINKING

        # Step 1: Analyze and create delegation plan
        plan = await self._create_delegation_plan(task)

        if not plan:
            return TaskResult(
                success=False,
                output="Failed to create a delegation plan.",
                error="Planning failed",
            )

        # Step 2: Execute the plan by delegating
        self.status = AgentStatus.DELEGATING
        results = await self._execute_plan(plan, task)

        # Step 3: Compile results
        self.status = AgentStatus.THINKING
        summary = await self._compile_results(task, results)

        # Step 4: Report
        self.status = AgentStatus.REPORTING
        await self._send_report(task, summary)

        return TaskResult(
            success=True,
            output=summary,
            data={
                "plan": plan,
                "delegation_count": len(results),
                "results": [r.to_dict() for r in results if r],
            },
        )

    async def _create_delegation_plan(self, task: Task) -> Optional[List[Dict[str, Any]]]:
        """
        Use LLM to analyze the task and create a delegation plan.
        This is where Jarvis's strategic thinking happens.
        """
        employee_info = "\n".join([
            f"- {name}: {info['role']} - Skills: {', '.join(info['skills'])}"
            for name, info in EMPLOYEE_CAPABILITIES.items()
        ])

        available = ", ".join(self.employees.keys()) if self.employees else "None registered yet"

        prompt = f"""あなたはJarvis（CSO）です。以下のタスクを分析し、部下に委譲するプランを作成してください。

## タスク
{task.description}

## コンテキスト
{json.dumps(task.context, ensure_ascii=False, default=str)}

## 利用可能な従業員
{employee_info}

## 現在稼働中の従業員
{available}

## 指示
1. タスクを分析し、必要なサブタスクに分解してください
2. 各サブタスクに最適な従業員を割り当ててください
3. 自分では作業しない。推論して委譲するだけ。

以下のJSON形式で回答してください（JSONのみ、説明不要）:
```json
[
    {{
        "employee": "従業員名",
        "subtask": "具体的なサブタスクの説明",
        "priority": 1-10の優先度,
        "depends_on": []
    }}
]
```"""

        try:
            response = await self.call_llm(prompt)

            # Extract JSON from response
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            plan = json.loads(json_str.strip())
            logger.info(f"Delegation plan created with {len(plan)} sub-tasks")
            return plan

        except (json.JSONDecodeError, IndexError) as e:
            logger.error(f"Failed to parse delegation plan: {e}")
            # Fallback: create a simple single-delegation plan
            return [{
                "employee": list(self.employees.keys())[0] if self.employees else "Alice",
                "subtask": task.description,
                "priority": 5,
                "depends_on": [],
            }]
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return None

    async def _execute_plan(
        self,
        plan: List[Dict[str, Any]],
        parent_task: Task,
    ) -> List[TaskResult]:
        """Execute the delegation plan by assigning tasks to employees."""
        results = []

        # Group by dependency level for parallel execution
        independent_tasks = [p for p in plan if not p.get("depends_on")]
        dependent_tasks = [p for p in plan if p.get("depends_on")]

        # Execute independent tasks in parallel
        if independent_tasks:
            parallel_results = await asyncio.gather(
                *[self._delegate_to_employee(item, parent_task) for item in independent_tasks],
                return_exceptions=True,
            )
            for r in parallel_results:
                if isinstance(r, TaskResult):
                    results.append(r)
                elif isinstance(r, Exception):
                    results.append(TaskResult(
                        success=False, output="", error=str(r)
                    ))

        # Execute dependent tasks sequentially
        for item in dependent_tasks:
            try:
                result = await self._delegate_to_employee(item, parent_task)
                results.append(result)
            except Exception as e:
                results.append(TaskResult(
                    success=False, output="", error=str(e)
                ))

        return results

    async def _delegate_to_employee(
        self,
        plan_item: Dict[str, Any],
        parent_task: Task,
    ) -> TaskResult:
        """Delegate a sub-task to a specific employee."""
        employee_name = plan_item["employee"]
        subtask_desc = plan_item["subtask"]
        priority = plan_item.get("priority", 5)

        employee = self.employees.get(employee_name)
        if not employee:
            logger.warning(f"Employee {employee_name} not found, creating virtual task")
            return TaskResult(
                success=False,
                output="",
                error=f"Employee {employee_name} is not available",
                agent_name=employee_name,
            )

        task_id = f"jarvis-{uuid.uuid4().hex[:8]}"

        # Create an event to wait for completion
        completion_event = asyncio.Event()
        self._pending_delegations[task_id] = completion_event

        # Create and assign the task
        sub_task = Task(
            id=task_id,
            description=subtask_desc,
            assigned_to=employee_name,
            assigned_by="Jarvis",
            priority=priority,
            context={
                "parent_task": parent_task.id,
                "parent_description": parent_task.description,
            },
        )

        await employee.assign_task(sub_task)

        logger.info(f"Delegated to {employee_name}: {subtask_desc[:60]}...")

        # Wait for completion (with timeout)
        try:
            await asyncio.wait_for(completion_event.wait(), timeout=120)
        except asyncio.TimeoutError:
            logger.warning(f"Delegation to {employee_name} timed out")

        # Get result
        result = self.delegation_results.pop(task_id, TaskResult(
            success=False,
            output="Task timed out",
            error="Timeout waiting for employee response",
            agent_name=employee_name,
        ))

        self._pending_delegations.pop(task_id, None)
        return result

    async def _on_task_completed(self, event: Event) -> None:
        """Handle task completion events from employees."""
        task_id = event.data.get("task_id", "")
        if task_id in self._pending_delegations:
            result_data = event.data.get("result", {})
            self.delegation_results[task_id] = TaskResult(
                success=result_data.get("success", True),
                output=result_data.get("output", ""),
                data=result_data.get("data", {}),
                agent_name=event.source,
            )
            self._pending_delegations[task_id].set()

    async def _on_task_failed(self, event: Event) -> None:
        """Handle task failure events from employees."""
        task_id = event.data.get("task_id", "")
        if task_id in self._pending_delegations:
            self.delegation_results[task_id] = TaskResult(
                success=False,
                output="",
                error=event.data.get("error", "Unknown error"),
                agent_name=event.source,
            )
            self._pending_delegations[task_id].set()

    async def _compile_results(
        self,
        task: Task,
        results: List[TaskResult],
    ) -> str:
        """Compile delegation results into a coherent summary."""
        results_text = "\n\n".join([
            f"### {r.agent_name or 'Unknown'}\n"
            f"Status: {'Success' if r.success else 'Failed'}\n"
            f"Output: {r.output[:500]}"
            for r in results
        ])

        prompt = f"""以下のタスクの結果をまとめてください。

## 元のタスク
{task.description}

## 各従業員の結果
{results_text}

簡潔にまとめた報告書を作成してください。"""

        try:
            summary = await self.call_llm(prompt)
            return summary
        except Exception as e:
            logger.error(f"Failed to compile results: {e}")
            return f"Results compiled (auto): {len(results)} tasks processed, {sum(1 for r in results if r.success)} succeeded."

    async def _send_report(self, task: Task, summary: str) -> None:
        """Send a report via Telegram (if configured)."""
        await self.event_bus.publish(Event(
            event_type=EventType.REPORT_GENERATED,
            source="Jarvis",
            data={
                "task_id": task.id,
                "task_description": task.description,
                "summary": summary,
            },
        ))

    async def call_llm(self, prompt: str, system: Optional[str] = None) -> str:
        """Call Claude Opus for Jarvis's reasoning."""
        try:
            import anthropic

            client = anthropic.AsyncAnthropic(api_key=self.config.anthropic.api_key)

            system_prompt = system or self.mindset

            # Add conversation context
            messages = []
            # Include recent history for context
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            messages.append({"role": "user", "content": prompt})

            response = await client.messages.create(
                model=self.config.anthropic.model_opus,
                max_tokens=self.config.anthropic.max_tokens,
                system=system_prompt,
                messages=messages,
            )

            result = response.content[0].text

            # Update history
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": result})

            # Track tokens
            self.total_tokens_used += response.usage.input_tokens + response.usage.output_tokens

            return result

        except ImportError:
            logger.warning("Anthropic library not installed, using mock response")
            return self._mock_llm_response(prompt)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return self._mock_llm_response(prompt)

    def _mock_llm_response(self, prompt: str) -> str:
        """Mock LLM response for testing without API keys."""
        if "delegation" in prompt.lower() or "プラン" in prompt or "委譲" in prompt:
            # Return a mock delegation plan
            employees = list(self.employees.keys()) if self.employees else ["Alice", "Max", "Sam"]
            plan = []
            for i, emp in enumerate(employees[:3]):
                plan.append({
                    "employee": emp,
                    "subtask": f"Sub-task {i+1} for the given objective",
                    "priority": 8 - i,
                    "depends_on": [],
                })
            return json.dumps(plan, indent=2)
        else:
            return (
                "## Task Report\n\n"
                "All sub-tasks have been delegated and completed.\n"
                "Results have been compiled and are ready for review.\n\n"
                "### Summary\n"
                "The team has successfully processed the assigned tasks. "
                "Each employee contributed their specialized skills to deliver "
                "comprehensive results."
            )

    async def get_team_status(self) -> Dict[str, Any]:
        """Get the status of all employees."""
        team_status = {}
        for name, employee in self.employees.items():
            team_status[name] = employee.get_status_dict()
        return {
            "jarvis": self.get_status_dict(),
            "employees": team_status,
            "total_employees": len(self.employees),
        }

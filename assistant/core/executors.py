from ..agent import Plan

from typing import List, Dict, Any, Optional
from ..agent import BaseAgent, AgentConfig, Plan
from ..agent.planner_agent import Task, Step, AgentStatus
from agents import RunResult
import asyncio


class PlanExecutor:
    """
    Executor class that receives a plan from the Planner and delegates tasks to sub-agents.
    """

    def __init__(self, sub_agents: List[BaseAgent]):
        """
        Initialize the executor with available sub-agents.

        Args:
            sub_agents: List of available sub-agents to execute tasks
        """
        self.sub_agents = sub_agents
        self._agent_registry = self._build_agent_registry()

    def _build_agent_registry(self) -> Dict[str, BaseAgent]:
        """Build a registry mapping agent names to agent instances."""
        registry = {}
        for agent in self.sub_agents:
            config: AgentConfig = agent.get_config()
            registry[config.name] = agent
        return registry

    async def execute_plan(
        self, plan: Plan, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the given plan by delegating tasks to appropriate sub-agents.

        Args:
            plan: The plan object containing steps and tasks to execute
            context: Optional context dictionary to share data between tasks

        Returns:
            Dictionary containing execution results and final context
        """
        if context is None:
            context = {}

        execution_results = {
            "steps": [],
            "context": context,
            "status": "success",
            "errors": [],
        }

        try:
            for step in plan.steps:
                step_result = await self._execute_step(step, context)
                execution_results["steps"].append(step_result)

                # Update context with step results
                context.update(step_result.get("context", {}))

                # Check if any critical errors occurred
                if step_result["status"] == "error" and step_result.get(
                    "critical", False
                ):
                    execution_results["status"] = "error"
                    execution_results["errors"].extend(step_result.get("errors", []))
                    break

        except Exception as e:
            execution_results["status"] = "error"
            execution_results["errors"].append(f"Plan execution failed: {str(e)}")

        return execution_results

    async def _execute_step(
        self, step: Step, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single step by running all its tasks in parallel.

        Args:
            step: The step containing tasks to execute
            context: Shared context dictionary

        Returns:
            Dictionary containing step execution results
        """
        step_result = {
            "step_number": step.step_number,
            "tasks": [],
            "status": "success",
            "context": {},
            "errors": [],
        }

        # Create tasks for parallel execution
        task_coroutines = []
        for task in step.tasks:
            if task.agent_type in self._agent_registry:
                task_coroutines.append(self._execute_task(task, context))
            else:
                error_msg = f"Agent type '{task.agent_type}' not found in registry"
                step_result["errors"].append(error_msg)
                step_result["status"] = "error"

        # Execute tasks in parallel
        if task_coroutines:
            task_results = await asyncio.gather(
                *task_coroutines, return_exceptions=True
            )

            for i, result in enumerate(task_results):
                if isinstance(result, Exception):
                    error_result = {
                        "task_description": step.tasks[i].description,
                        "agent_type": step.tasks[i].agent_type,
                        "status": "error",
                        "error": str(result),
                        "result": None,
                    }
                    step_result["tasks"].append(error_result)
                    step_result["errors"].append(str(result))
                    step_result["status"] = "error"
                else:
                    step_result["tasks"].append(result)
                    # Merge task context into step context
                    if "context" in result:
                        step_result["context"].update(result["context"])

        return step_result

    async def _execute_task(
        self, task: Task, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single task using the appropriate sub-agent.

        Args:
            task: The task to execute
            context: Shared context dictionary

        Returns:
            Dictionary containing task execution results
        """
        task_result = {
            "task_description": task.description,
            "agent_type": task.agent_type,
            "status": "working",
            "result": None,
            "context": {},
        }

        try:
            # Update task status
            task.status = AgentStatus.WORKING

            # Get the appropriate agent
            agent = self._agent_registry[task.agent_type]

            # Prepare input with context
            task_input = {"query": task.description, "context": context}

            # Execute the task
            result: RunResult = await agent.run(task_input)

            # Process the result
            task_result["status"] = "completed"
            task_result["result"] = (
                result.data if hasattr(result, "data") else str(result)
            )
            task.status = AgentStatus.COMPLETED

            # Extract any context updates from the result
            if hasattr(result, "context") and result.context:
                task_result["context"] = result.context

        except Exception as e:
            task_result["status"] = "error"
            task_result["error"] = str(e)
            task.status = AgentStatus.ERROR

        return task_result

    def get_available_agents(self) -> List[str]:
        """Return list of available agent types."""
        return list(self._agent_registry.keys())

    def get_agent_config(self, agent_type: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent type."""
        if agent_type in self._agent_registry:
            return self._agent_registry[agent_type].get_config()
        return None

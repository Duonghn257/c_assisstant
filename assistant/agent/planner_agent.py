from pydantic import BaseModel, Field
from typing import List, Dict, Union
from agents import Agent, FunctionTool, RunResult, Runner

from .base import BaseAgent, AgentConfig
from .model import init_llm, Model
from enum import Enum


class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    ERROR = "error"


class Task(BaseModel):
    agent_type: str = Field(
        ..., description="The agent is required for this sub-task."
    )  # TODO: generalize by List[AgentType], not str
    description: str = Field(..., description="A clear description of the task.")
    status: AgentStatus = Field(
        default=AgentStatus.IDLE,
        description="The status of the task.",
    )


class Step(BaseModel):
    step_number: int = Field(..., description="The sequential number of the step.")
    tasks: List[Task] = Field(
        ..., description="A list of independent tasks to be performed within this step."
    )


class Plan(BaseModel):
    steps: List[Step] = Field(
        ..., description="A list of sequential steps to accomplish the plan."
    )


class Planner:
    name = "Planner Agent"

    def __init__(
        self, *, model: Model, sub_agents: List[BaseAgent] | None = None, **agent_kwargs
    ):
        self.sub_agents = sub_agents

        self.agent = Agent(
            name=self.name,
            model=init_llm(model),
            instructions=self._get_instructions(),
            output_type=Plan,
            **agent_kwargs,
        )

    def _get_instructions(self) -> str:
        if not self.sub_agents:
            return """You are a Planner Agent responsible for breaking down complex tasks into structured plans.

            Your output must be a Plan containing sequential Steps, where each Step contains Tasks that can be executed in parallel.

            Return your response as a Plan object with the following structure:
            - steps: List of Step objects
            - Each Step has: step_number (int) and tasks (List[Task])
            - Each Task has: agent_type (str), description (str), and status (defaults to IDLE)

            Available agent types: None (no sub-agents configured)
            """

        # Collect agent configurations
        agent_descriptions = []
        for agent in self.sub_agents:
            agent_config: AgentConfig = agent.get_config()
            agent_descriptions.append(
                f"- {agent_config.name}: {agent_config.description}"
            )

        available_agents = "\n".join(agent_descriptions)

        return f"""You are a Planner Agent responsible for breaking down complex tasks into structured, executable plans.

        Your role is to analyze user queries and create detailed plans using the available sub-agents. \
        Each plan should be logical, efficient, and leverage the specific capabilities of each agent.

        Available Sub-Agents:
        {available_agents}

        Your output must be a Plan containing sequential Steps, where each Step contains Tasks that can be executed in parallel within that step.

        Return your response as a Plan object with the following structure:
        - steps: List of Step objects in sequential order
        - Each Step has: step_number (int) and tasks (List[Task])
        - Each Task has: agent_type (str - must match one of the available agent names), description (str - clear, actionable task description), \
        and status (defaults to IDLE)

        Guidelines:
        1. Break down complex queries into logical, sequential steps
        2. Within each step, identify tasks that can be performed in parallel
        3. Ensure each task is assigned to the most appropriate agent based on their capabilities
        4. Make task descriptions clear and actionable
        5. Consider dependencies between steps - later steps should build on earlier ones
        6. Optimize for efficiency while maintaining logical flow
        7. All tasks should start with status IDLE
        """

    async def create_plan(self, query: str, **kwargs) -> RunResult:
        return await Runner.run(self.agent, input=query, **kwargs)


def main():
    planner = Planner()
    print(planner)

    pass


if __name__ == "__main__":
    main()

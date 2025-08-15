from pydantic import BaseModel, Field
from typing import List, Dict, Union
from agents import Agent, FunctionTool, RunResult, RunResultStreaming

from .base import BaseAgent
from .helpers import init_llm, Model

class Task(BaseModel):
    agent_type: str = Field(..., description="The agent is required for this sub-task.")     # TODO: generalize by List[AgentType], not str
    description: str = Field(..., description="A clear description of the task.")

class Step(BaseModel):
    step_number: int = Field(..., description="The sequential number of the step.")
    tasks: List[Task] = Field(..., description="A list of independent tasks to be performed within this step.")

class Plan(BaseModel):
    steps: List[Step] = Field(..., description="A list of sequential steps to accomplish the plan.")
    
class Planner(BaseAgent):
    name = "PlannerAgent"

    def __init__(
        self,
        *,
        model: Model,
        instructions: str | None = None,
        tools: List[FunctionTool] | None = None,
        **agent_kwargs
    ):
        super().__init__(
            name=self.name, # Lấy name từ class attribute
            model=model,
            instructions=instructions,
            tools=tools,
            **agent_kwargs
        )

    def invoke(self, query: str, **kwargs) -> RunResult:
        return super().invoke(query, **kwargs)

    async def run_async(self, query: str, **kwargs) -> RunResult:
        return await super().run_async(query, **kwargs)

    async def run_streaming(self, query: str, **kwargs) -> RunResultStreaming:
        return super().run_streaming(query, **kwargs)

def main():
    planner = Planner(
        model=Model('azure/gpt-4o-mini'),
        instructions="""Planner agent""",
        output_type=List[str]
    )
    print(planner)

    pass

if __name__ == "__main__":
    main()
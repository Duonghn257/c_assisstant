from .base import BaseAgent
from agents import Tool, function_tool, Agent, RunResult, RunResultStreaming
from .tools.tool_manager import ToolManager
from .helpers import Model
from typing import List
from agents import FunctionTool
from agents.extensions.models.litellm_model import LitellmModel

class ShapeAgent(BaseAgent):
    name: str = "Shape Agent"

    def __init__(
        self,
        *,
        model: LitellmModel,
        instructions: str | None = None,
        tools: List[FunctionTool] | None = None,
    ):
        super().__init__(name=self.name, model=model, instructions=instructions, tools=tools)

    def __str__(self):
        return f"Agent Name: {self.name} \nModel use:{self.model}\nTools use:{self.tools}"

    def invoke(self, query: str, **kwargs) -> RunResult:
        return super().invoke(query, **kwargs)

    async def run_async(self, query: str, **kwargs) -> RunResult:
        return await super().run_async(query, **kwargs)

    async def run_streaming(self, query: str, **kwargs) -> RunResultStreaming:
        return super().run_streaming(query, **kwargs)

if __name__ == "__main__":
    tool_manager = ToolManager()

    mathagent = ShapeAgent(
        model=Model.AZURE_OPENAI_4oMINI,
        tools= tool_manager.get_tools_by_group("ShapeAreaTools")
    )

    print(mathagent.from_config())
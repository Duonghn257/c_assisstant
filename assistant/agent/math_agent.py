from .base import BaseAgent
from agents import Tool, function_tool, Agent, RunResult, RunResultStreaming
from .tools import ToolRegistry
from .helpers import Model

from typing import List
from agents import FunctionTool
from agents.extensions.models.litellm_model import LitellmModel

from loguru import logger


class MathAgent(BaseAgent):
    name: str = "Math Agent"
    tool_name: str = "MathTools"

    def __init__(
        self,
        *,
        model: Model,
        description: str,
        instructions: str,
        abilities: List[str],
        time_out: int,
        tools: List[FunctionTool] | None = None,
        **agents_kwargs,
    ):
        super().__init__(
            name=self.name,
            model=model,
            description=description,
            instructions=instructions,
            abilities=abilities,
            time_out=time_out,
            tools=tools,
            **agents_kwargs,
        )

    def invoke(self, query: str, **kwargs) -> RunResult:
        logger.info(f"MathAgent invoke: {query}")
        return super().invoke(query, **kwargs)

    async def run_async(self, query: str, **kwargs) -> RunResult:
        return await super().run_async(query, **kwargs)

    async def run_streaming(self, query: str, **kwargs) -> RunResultStreaming:
        return super().run_streaming(query, **kwargs)

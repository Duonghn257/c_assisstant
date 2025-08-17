from dataclasses import dataclass
import inspect
import os
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict
from agents import Agent, FunctionTool, RunResult, RunResultStreaming, Runner
from .model import Model, init_llm
from agents.extensions.models.litellm_model import LitellmModel
from enum import Enum
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    name: str = Field(..., description="The name of the agent.")
    model: str = Field(..., description="The model of the agent.")
    abilities: List[str] = Field(..., description="The abilities of the agent.")
    description: str = Field(..., description="The description of the agent.")
    instructions: str = Field(..., description="The instructions of the agent.")
    time_out: int = Field(..., description="The time out of the agent.")


class BaseAgent(ABC):
    """An abstract base class for all agents."""

    _openai_agent_allowed_params: Optional[Dict[str, inspect.Parameter]] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()

        if not hasattr(cls, "name"):
            raise TypeError(
                f"Class {cls.__name__} must define 'name' as class attribute."
            )

        if not isinstance(cls.name, str):
            raise TypeError(
                f"Attribute 'name` must be of type str, got {type(cls.name)}"
            )

        if BaseAgent._openai_agent_allowed_params is None:
            sig = inspect.signature(Agent.__init__)

            BaseAgent._openai_agent_allowed_params = {
                name: param for name, param in sig.parameters.items() if name != "self"
            }

    def __init__(
        self,
        *,
        name: str,
        model: Model,
        description: str,
        instructions: str,
        abilities: List[str],
        time_out: int,
        tools: List[FunctionTool] | None = None,
        **agents_kwargs,
    ):
        self.name = name
        self.model = model
        self.description = description
        self.instructions = instructions
        self.abilities = abilities
        self.time_out = time_out
        self.tools = tools

        agent_param = {
            "name": name,
            "model": init_llm(model),
            "instructions": instructions,
        }

        if tools:
            agent_param["tools"] = tools
            self.tools = tools

        if agents_kwargs:
            for key in agents_kwargs:
                if key not in BaseAgent._openai_agent_allowed_params:

                    allowed_keys = ", ".join(
                        BaseAgent._openai_agent_allowed_params.keys()
                    )
                    raise ValueError(
                        f"Unsupported parameter '{key}' passed to BaseAgent for OpenAI Agent.\n"
                        f"Allowed parameters are: {allowed_keys}"
                    )

            agent_param.update(agents_kwargs)

        self.agent = Agent(**agent_param)

    def __str__(self):
        return f"""Agent name: {self.name}\nAgent Properties: \n{self.agent}"""

    def get_config(self) -> AgentConfig:
        return AgentConfig(
            name=self.name,
            model=self.model,
            abilities=self.abilities,
            description=self.description,
            instructions=self.instructions,
            time_out=self.time_out,
        )

    @abstractmethod
    def invoke(self, query: str, **kwargs) -> RunResult:
        return Runner.run_sync(self.agent, query, **kwargs)

    @abstractmethod
    async def run_async(self, query: str, **kwargs) -> RunResult:
        return await Runner.run_async(self.agent, query, **kwargs)

    @abstractmethod
    async def run_streaming(self, query: str, **kwargs) -> RunResultStreaming:
        return await Runner.run_streaming(self.agent, query, **kwargs)

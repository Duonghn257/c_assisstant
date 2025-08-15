from dataclasses import dataclass
import inspect
import os
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict
from agents import Agent, FunctionTool, RunResult, RunResultStreaming, Runner
from .helpers import Model, init_llm
from agents.extensions.models.litellm_model import LitellmModel
from enum import Enum
import yaml

@dataclass
class AgentConfig():
    model: str
    abilities: List[str]
    description: str
    instructions: str
    
class BaseAgent(ABC):
    """An abstract base class for all agents."""
    _openai_agent_allowed_params: Optional[Dict[str, inspect.Parameter]] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        
        if not hasattr(cls, "name"):
            raise TypeError(f"Class {cls.__name__} must define 'name' as class attribute.")

        if not isinstance(cls.name, str):
            raise TypeError(f"Attribute 'name` must be of type str, got {type(cls.name)}")

        if BaseAgent._openai_agent_allowed_params is None:
            sig = inspect.signature(Agent.__init__)

            BaseAgent._openai_agent_allowed_params = {
                name: param for name, param in sig.parameters.items() if name != 'self'
            }
            # print(f"DEBUG: Allowed OpenAI Agent params: {list(BaseAgent._openai_agent_allowed_params.keys())}")
            
    def __init__(
        self,
        *, 
        name: str, 
        model: Model, 
        instructions: str | None = None,
        tools: List[FunctionTool] | None = None,
        **agents_kwargs,
    ):
        agent_param = {
            "name": name,
            "model": init_llm(model),
            "instructions": instructions,
        }

        if tools:
            agent_param["tools"] = tools

        if agents_kwargs:
            for key in agents_kwargs:
                if key not in BaseAgent._openai_agent_allowed_params:
                    
                    allowed_keys = ", ".join(BaseAgent._openai_agent_allowed_params.keys())
                    raise ValueError(
                        f"Unsupported parameter '{key}' passed to BaseAgent for OpenAI Agent.\n"
                        f"Allowed parameters are: {allowed_keys}"
                    )

            agent_param.update(agents_kwargs) 

        self.agent = Agent(**agent_param)

    def __str__(self):
        return f"""Agent name: {self.name}\nAgent Properties: \n{self.agent}"""

    @classmethod
    def from_config(cls) -> AgentConfig:
        """
        Load and return the AgentConfig for this agent class from the YAML config file.
        Reads model, abilities, description, instructions from ..configs.config_files.agent_configs.yml.
        """
        # Determine the config file path relative to this file
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "configs", "config_files", "agent_configs.yml"
        )
        config_path = os.path.normpath(config_path)

        # Load YAML config
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Use the class's name as the key (e.g., "Shape Agent", "Math Agent", etc.)
        agent_key = getattr(cls, "name", None)
        if not agent_key:
            raise ValueError(f"Class {cls.__name__} must define a 'name' class attribute.")

        agent_config = config.get(agent_key)
        if not agent_config:
            raise ValueError(f"No configuration found for agent '{agent_key}' in {config_path}")

        # Extract fields
        model = agent_config.get("model")
        abilities = agent_config.get("abilities")
        description = agent_config.get("description")
        instructions = agent_config.get("instructions")
        
        # Return an AgentConfig instance
        return AgentConfig(
            model=model,
            abilities=abilities,
            description=description,
            instructions=instructions,
        )

    @abstractmethod
    def invoke(self, query: str, **kwargs) -> RunResult:
        return Runner.run_sync(self.agent, query, **kwargs)

    @abstractmethod
    async def run_async(self, query: str, **kwargs) -> RunResult:
        return await Runner.run_sync(self.agent, query, **kwargs)

    @abstractmethod
    async def run_streaming(self, query: str, **kwargs) -> RunResultStreaming:
        return await Runner.run_streaming(self.agent, query, **kwargs)
from ast import Dict
from collections import defaultdict
from .base import BaseAgent
from .math_agent import MathAgent
from .shape_agent import ShapeAgent
from ..utils.config_loader import ConfigLoader
from .tools.tool_manager import ToolRegistry
from typing import Type
from pydantic import Field, BaseModel
from typing import List
from enum import Enum
from loguru import logger


class AgentName(str, Enum):
    MATH_AGENT = "Math Agent"
    SHAPE_AGENT = "Shape Agent"


class AgentFactory:

    agents: dict[str, BaseAgent] = defaultdict(BaseAgent)
    agent_classes: dict[str, Type[BaseAgent]] = {}
    tool_registry = ToolRegistry()

    def get_agent(self, agent_name: str) -> BaseAgent:
        return self.agents[agent_name]

    def register_agent(self, agent_name: AgentName, overwrite: bool = False):
        available_agents = [t.value for t in AgentName]

        if agent_name == AgentName.MATH_AGENT:
            agent_class = MathAgent
        elif agent_name == AgentName.SHAPE_AGENT:
            agent_class = ShapeAgent
        else:
            raise ValueError(
                f"Unknown agent_name '{agent_name}'. Must be one of: {', '.join(available_agents)}"
            )

        agent_name_value = agent_name.value

        if agent_name_value in self.agent_classes and not overwrite:
            raise ValueError(
                f"Agent '{agent_name_value}' already registered. Use overwrite=True to replace."
            )

        self.agent_classes[agent_name_value] = agent_class

    def initialize_agents(self):
        """
        Initialize all registered agent classes and store their instances in self.agents.
        """
        config = ConfigLoader().config
        print(config)
        for agent_name, agent_class in self.agent_classes.items():
            agent_config = config[agent_name]
            logger.info(f"Initializing agent {agent_name} config")
            self.tool_registry.register_tool(agent_class.tool_name)
            self.agents[agent_name] = agent_class(
                **agent_config,
                tools=self.tool_registry.get_tools(agent_class.tool_name),
            )


if __name__ == "__main__":
    agent_factory = AgentFactory()
    agent_factory.register_agent(MathAgent)
    agent_factory.register_agent(ShapeAgent)
    agent_factory.initialize_agents()
    print(agent_factory.agents[AgentName.MATH_AGENT.value])

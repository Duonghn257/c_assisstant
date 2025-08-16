# tools/tool_manager.py
from collections import defaultdict
from typing import Dict, Type, List, Any, Optional, Protocol, TypeVar
from agents import FunctionTool
from dataclasses import dataclass, field
from .tool import MathTools, ShapeTools
from .tool import BaseTool, ToolName


@dataclass
class ToolDescription:
    name: str
    description: str
    parameters_schema: Dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, BaseTool] = defaultdict(BaseTool)

    def register_tool(self, toolName: str):
        available_tools = [t.value for t in ToolName]

        if toolName not in self.tools:
            if toolName == ToolName.MathTools.value:
                self.tools[toolName] = MathTools()
            elif toolName == ToolName.ShapeTools.value:
                self.tools[toolName] = ShapeTools()
            else:
                raise ValueError(
                    f"Tool '{toolName}' not found. Available tool names: {', '.join(available_tools)}"
                )
        else:
            raise ValueError(
                f"Tool '{toolName}' already registered. Available tool names: {', '.join(available_tools)}"
            )

    def get_tools(self, tool_name: str) -> List[FunctionTool]:
        return self.tools[tool_name].get_tools()

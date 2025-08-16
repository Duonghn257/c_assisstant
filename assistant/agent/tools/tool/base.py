from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union
from agents import Tool, function_tool, FunctionTool
from enum import Enum


class ToolName(Enum):
    MathTools = "MathTools"
    ShapeTools = "ShapeTools"


class BaseTool(ABC):
    """An abstract base class for all tools."""

    name: str = None
    description: str = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "name"):
            raise TypeError(
                f"Class {cls.__name__} must define 'name' as class attribute."
            )

        if not isinstance(cls.name, str):
            raise TypeError(
                f"Attribute 'name` must be of type str, got {type(cls.name)}"
            )

    def __str__(self) -> str:
        return f"Tool Group: {self.__class__.__name__}"

    @abstractmethod
    def get_tools(self, human_in_loop: bool = False) -> List[FunctionTool]:
        pass

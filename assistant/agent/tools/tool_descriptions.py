from dataclasses import dataclass, field
from typing import Dict, Type, List, Any, Optional, Protocol, TypeVar
from agents import FunctionTool

@dataclass
class ToolDescription:
    name: str
    description: str
    parameters_schema: Dict[str, Any] = field(default_factory=dict)
    

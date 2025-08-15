# tools/tool_manager.py

from typing import Dict, Type, List, Any, Optional, Protocol, TypeVar
from agents import FunctionTool
from dataclasses import dataclass, field
from .tool import MathTools, ShapeAreaTools
 
@dataclass
class ToolDescription:
    name: str
    description: str
    parameters_schema: Dict[str, Any] = field(default_factory=dict)
    
class ToolManager:
    """
    Manages the registration and retrieval of OpenAI FunctionTools.
    Automatically loads tools from MathTools and ShapeAreaTools via their get_tools classmethod.
    """
    _all_function_tools: Dict[str, FunctionTool] = {}
    _tools_by_group: Dict[str, List[FunctionTool]] = {}
    _is_initialized = False

    def __init__(self, **dependencies):
        """
        Initializes the ToolManager.
        This constructor should be called once, typically during application startup,
        to collect all available FunctionTools.
        
        Args:
            **dependencies: Any common dependencies that tool methods might need (e.g., database clients, API clients).
                            These will be passed to the tool group class's constructor.
        """
        if not ToolManager._is_initialized:
            self.dependencies = dependencies
            self._initialize_tools()
            ToolManager._is_initialized = True
        else:
            raise RuntimeError("ToolManager is already initialized")

    def _initialize_tools(self):
        """
        Automatically instantiate and collect tools from MathTools and ShapeAreaTools.
        """
        tool_group_classes = [MathTools, ShapeAreaTools]
        for tool_group_cls in tool_group_classes:
            # Instantiate the tool group, passing dependencies if needed
            try:
                tool_group_instance = tool_group_cls(**self.dependencies)
            except TypeError:
                tool_group_instance = tool_group_cls()
            group_name = getattr(tool_group_instance, "name", tool_group_cls.__name__)
            
            # # Get tools from the group
            if hasattr(tool_group_instance, "get_tools"):
                tools = tool_group_instance.get_tools()
                ToolManager._tools_by_group[group_name] = tools
                for tool in tools:
                    if tool.name in ToolManager._all_function_tools:
                        print(f"Warning: Duplicate function tool name found: {tool.name} in {group_name}. Overwriting in _all_function_tools.")
                    ToolManager._all_function_tools[tool.name] = tool

    def get_function_tool(self, tool_name: str) -> Optional[FunctionTool]:
        """
        Retrieves a specific FunctionTool by its name.
        """
        return ToolManager._all_function_tools.get(tool_name)

    def get_all_function_tools(self) -> List[FunctionTool]:
        """
        Returns a list of all registered FunctionTool instances.
        This list can be passed directly to agent.add_tool().
        """
        return list(ToolManager._all_function_tools.values())

    def get_tools_by_group(self, group_name: str) -> List[FunctionTool]:
        """
        Returns a list of FunctionTool instances belonging to a specific tool group.
        
        Args:
            group_name (str): The name of the tool group class (e.g., "MathTools", "ShapeAreaTools").

        Returns:
            List[FunctionTool]: A list of FunctionTool instances, or an empty list if group not found.
        """
        tools = ToolManager._tools_by_group.get(group_name)
        if tools is None:
            available_groups = list(ToolManager._tools_by_group.keys())
            print(f"Warning: Tool group '{group_name}' not found.")
            if available_groups:
                print(f"Available tool groups are: {', '.join(available_groups)}")
            else:
                print("No tool groups are currently registered.")
            return []
        return tools

    def get_tool_description(self, tool_name: str) -> ToolDescription:
        tool = ToolManager._all_function_tools.get(tool_name)
        description = tool.description if tool and hasattr(tool, "description") else ""
        return ToolDescription(
            name=tool_name,
            description=description
        )

def main():
    toolmanager = ToolManager()
    print(toolmanager.get_tools_by_group("MathTools"))
if __name__ == "__main__":
    main()
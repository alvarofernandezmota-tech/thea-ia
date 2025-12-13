"""
H08.4 - Tool Calling System
Manages tool definitions, execution, and validation
"""

from typing import Callable, Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import asyncio


class ToolType(str, Enum):
    """Tool execution type"""
    SYNC = "sync"
    ASYNC = "async"


@dataclass
class ToolParameter:
    """Represents a tool parameter"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None


@dataclass
class Tool:
    """Represents a callable tool"""
    name: str
    description: str
    func: Callable
    parameters: List[ToolParameter] = field(default_factory=list)
    tool_type: ToolType = ToolType.SYNC
    category: str = "general"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for LLM"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default
                }
                for p in self.parameters
            ]
        }


class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        """Initialize tool registry"""
        self.tools: Dict[str, Tool] = {}
        self.categories: Dict[str, List[str]] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool"""
        self.tools[tool.name] = tool
        
        # Add to category
        if tool.category not in self.categories:
            self.categories[tool.category] = []
        self.categories[tool.category].append(tool.name)
    
    def register_function(
        self,
        func: Callable,
        name: str,
        description: str,
        parameters: Optional[List[ToolParameter]] = None,
        tool_type: ToolType = ToolType.SYNC,
        category: str = "general"
    ) -> Tool:
        """Register a function as a tool"""
        tool = Tool(
            name=name,
            description=description,
            func=func,
            parameters=parameters or [],
            tool_type=tool_type,
            category=category
        )
        self.register(tool)
        return tool
    
    def get(self, name: str) -> Optional[Tool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def get_all(self) -> List[Tool]:
        """Get all tools"""
        return list(self.tools.values())
    
    def get_by_category(self, category: str) -> List[Tool]:
        """Get tools by category"""
        tool_names = self.categories.get(category, [])
        return [self.tools[name] for name in tool_names]
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all tools as dicts for LLM"""
        return [tool.to_dict() for tool in self.get_all()]
    
    def list_categories(self) -> List[str]:
        """List all categories"""
        return list(self.categories.keys())


class ToolExecutor:
    """Executes tools with validation and error handling"""
    
    def __init__(self, registry: ToolRegistry):
        """Initialize executor"""
        self.registry = registry
    
    async def execute(
        self,
        tool_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a tool
        
        Args:
            tool_name: Name of tool to execute
            **kwargs: Tool parameters
        
        Returns:
            Execution result with status and output
        """
        tool = self.registry.get(tool_name)
        
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "output": None
            }
        
        # Validate parameters
        validation = self._validate_parameters(tool, kwargs)
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"],
                "output": None
            }
        
        # Execute tool
        try:
            if tool.tool_type == ToolType.ASYNC:
                result = await tool.func(**kwargs)
            else:
                result = tool.func(**kwargs)
            
            return {
                "success": True,
                "tool": tool_name,
                "output": result,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "tool": tool_name,
                "output": None,
                "error": str(e)
            }
    
    def _validate_parameters(
        self,
        tool: Tool,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate tool parameters"""
        provided_keys = set(params.keys())
        required_params = {p.name for p in tool.parameters if p.required}
        optional_params = {p.name for p in tool.parameters if not p.required}
        
        # Check required parameters
        missing = required_params - provided_keys
        if missing:
            return {
                "valid": False,
                "error": f"Missing required parameters: {', '.join(missing)}"
            }
        
        # Check unexpected parameters
        allowed = required_params | optional_params
        extra = provided_keys - allowed
        if extra:
            return {
                "valid": False,
                "error": f"Unexpected parameters: {', '.join(extra)}"
            }
        
        return {"valid": True, "error": None}


class ToolChain:
    """Chains multiple tools for sequential execution"""
    
    def __init__(self, executor: ToolExecutor):
        """Initialize tool chain"""
        self.executor = executor
        self.steps: List[Dict[str, Any]] = []
    
    def add_step(
        self,
        tool_name: str,
        **kwargs
    ) -> "ToolChain":
        """Add step to chain"""
        self.steps.append({
            "tool": tool_name,
            "params": kwargs
        })
        return self
    
    async def execute(self) -> List[Dict[str, Any]]:
        """Execute all steps in chain"""
        results = []
        
        for i, step in enumerate(self.steps):
            result = await self.executor.execute(
                step["tool"],
                **step["params"]
            )
            results.append(result)
            
            # Stop if step failed and it's required
            if not result["success"]:
                break
        
        return results
    
    def clear(self) -> None:
        """Clear chain steps"""
        self.steps = []

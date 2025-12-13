"""
Tests for Tool Calling System (H08.4)
"""

import pytest
from theaia.core.conversation.tools import (
    Tool,
    ToolParameter,
    ToolRegistry,
    ToolExecutor,
    ToolChain,
    ToolType
)


class TestToolParameter:
    """Test ToolParameter class"""
    
    def test_parameter_creation(self):
        """Test creating parameter"""
        param = ToolParameter(
            name="query",
            type="str",
            description="Search query"
        )
        assert param.name == "query"
        assert param.type == "str"
        assert param.required is True


class TestTool:
    """Test Tool class"""
    
    def test_tool_creation(self):
        """Test creating tool"""
        def dummy_func(x: int) -> int:
            return x * 2
        
        tool = Tool(
            name="double",
            description="Double a number",
            func=dummy_func
        )
        assert tool.name == "double"
        assert tool.func(5) == 10
    
    def test_tool_with_parameters(self):
        """Test tool with parameters"""
        def add(a: int, b: int) -> int:
            return a + b
        
        params = [
            ToolParameter("a", "int", "First number"),
            ToolParameter("b", "int", "Second number")
        ]
        
        tool = Tool(
            name="add",
            description="Add two numbers",
            func=add,
            parameters=params
        )
        
        assert len(tool.parameters) == 2
    
    def test_tool_to_dict(self):
        """Test converting tool to dict"""
        def greet(name: str) -> str:
            return f"Hello {name}"
        
        params = [ToolParameter("name", "str", "Person's name")]
        tool = Tool(
            name="greet",
            description="Greet someone",
            func=greet,
            parameters=params,
            category="greeting"
        )
        
        tool_dict = tool.to_dict()
        assert tool_dict["name"] == "greet"
        assert tool_dict["category"] == "greeting"
        assert len(tool_dict["parameters"]) == 1


class TestToolRegistry:
    """Test ToolRegistry class"""
    
    def test_registry_creation(self):
        """Test creating registry"""
        registry = ToolRegistry()
        assert len(registry.get_all()) == 0
    
    def test_register_tool(self):
        """Test registering tool"""
        def dummy(): pass
        
        registry = ToolRegistry()
        tool = Tool("test", "Test tool", dummy)
        registry.register(tool)
        
        assert registry.get("test") == tool
        assert len(registry.get_all()) == 1
    
    def test_register_function(self):
        """Test registering function"""
        def multiply(a: int, b: int) -> int:
            return a * b
        
        registry = ToolRegistry()
        params = [
            ToolParameter("a", "int", "First number"),
            ToolParameter("b", "int", "Second number")
        ]
        
        tool = registry.register_function(
            multiply,
            "multiply",
            "Multiply numbers",
            parameters=params
        )
        
        assert tool.name == "multiply"
        assert registry.get("multiply") is not None
    
    def test_get_by_category(self):
        """Test getting tools by category"""
        def tool1(): pass
        def tool2(): pass
        
        registry = ToolRegistry()
        registry.register(Tool("t1", "Tool 1", tool1, category="math"))
        registry.register(Tool("t2", "Tool 2", tool2, category="math"))
        
        math_tools = registry.get_by_category("math")
        assert len(math_tools) == 2
    
    def test_list_categories(self):
        """Test listing categories"""
        def dummy(): pass
        
        registry = ToolRegistry()
        registry.register(Tool("t1", "Tool 1", dummy, category="cat1"))
        registry.register(Tool("t2", "Tool 2", dummy, category="cat2"))
        
        categories = registry.list_categories()
        assert "cat1" in categories
        assert "cat2" in categories


class TestToolExecutor:
    """Test ToolExecutor class"""
    
    def test_executor_creation(self):
        """Test creating executor"""
        registry = ToolRegistry()
        executor = ToolExecutor(registry)
        assert executor.registry == registry
    
    @pytest.mark.asyncio
    async def test_execute_simple_tool(self):
        """Test executing simple tool"""
        def add(a: int, b: int) -> int:
            return a + b
        
        registry = ToolRegistry()
        params = [
            ToolParameter("a", "int", "First"),
            ToolParameter("b", "int", "Second")
        ]
        registry.register_function(add, "add", "Add", params)
        
        executor = ToolExecutor(registry)
        result = await executor.execute("add", a=2, b=3)
        
        assert result["success"] is True
        assert result["output"] == 5
    
    @pytest.mark.asyncio
    async def test_execute_nonexistent_tool(self):
        """Test executing nonexistent tool"""
        registry = ToolRegistry()
        executor = ToolExecutor(registry)
        result = await executor.execute("nonexistent")
        
        assert result["success"] is False
        assert "not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_missing_required_parameter(self):
        """Test missing required parameter"""
        def greet(name: str) -> str:
            return f"Hello {name}"
        
        registry = ToolRegistry()
        params = [ToolParameter("name", "str", "Name")]
        registry.register_function(greet, "greet", "Greet", params)
        
        executor = ToolExecutor(registry)
        result = await executor.execute("greet")
        
        assert result["success"] is False
        assert "Missing required" in result["error"]
    
    @pytest.mark.asyncio
    async def test_tool_execution_error(self):
        """Test tool execution error"""
        def failing_tool():
            raise ValueError("Test error")
        
        registry = ToolRegistry()
        registry.register(Tool("fail", "Failing", failing_tool))
        
        executor = ToolExecutor(registry)
        result = await executor.execute("fail")
        
        assert result["success"] is False
        assert "Test error" in result["error"]


class TestToolChain:
    """Test ToolChain class"""
    
    def test_chain_creation(self):
        """Test creating chain"""
        registry = ToolRegistry()
        executor = ToolExecutor(registry)
        chain = ToolChain(executor)
        
        assert len(chain.steps) == 0
    
    def test_add_step(self):
        """Test adding step to chain"""
        registry = ToolRegistry()
        executor = ToolExecutor(registry)
        chain = ToolChain(executor)
        
        chain.add_step("tool1", param1="value1")
        assert len(chain.steps) == 1
    
    def test_chain_fluent_api(self):
        """Test chain fluent API"""
        registry = ToolRegistry()
        executor = ToolExecutor(registry)
        
        chain = (ToolChain(executor)
                .add_step("tool1", x=1)
                .add_step("tool2", y=2))
        
        assert len(chain.steps) == 2
    
    @pytest.mark.asyncio
    async def test_chain_execution(self):
        """Test executing chain"""
        def add(a: int, b: int) -> int:
            return a + b
        
        registry = ToolRegistry()
        params = [
            ToolParameter("a", "int", "First"),
            ToolParameter("b", "int", "Second")
        ]
        registry.register_function(add, "add", "Add", params)
        
        executor = ToolExecutor(registry)
        chain = ToolChain(executor)
        chain.add_step("add", a=1, b=2)
        chain.add_step("add", a=3, b=4)
        
        results = await chain.execute()
        assert len(results) == 2
        assert results[0]["output"] == 3
        assert results[1]["output"] == 7
    
    def test_chain_clear(self):
        """Test clearing chain"""
        registry = ToolRegistry()
        executor = ToolExecutor(registry)
        chain = ToolChain(executor)
        
        chain.add_step("tool1")
        chain.clear()
        
        assert len(chain.steps) == 0

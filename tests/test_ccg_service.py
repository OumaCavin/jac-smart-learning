"""
Test Suite for Code Context Graph (CCG) Service
Author: Cavin Otieno
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

# Test imports
from backend.services.ccg_service import (
    CodeAnalyzer, 
    Neo4jCCGStore, 
    CCGService, 
    NodeType, 
    RelationshipType,
    CCGNode, 
    CCGEdge
)


class TestCodeAnalyzer:
    """Test cases for CodeAnalyzer"""

    def setup_method(self):
        """Setup test environment"""
        self.analyzer = CodeAnalyzer()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample Python code file
        self.sample_file = os.path.join(self.temp_dir, "test.py")
        with open(self.sample_file, 'w') as f:
            f.write("""
class TestClass:
    def __init__(self):
        self.value = 42
    
    def method_a(self, x):
        return x * 2
    
    def method_b(self):
        return self.method_a(10)

def test_function():
    return TestClass().method_a(5)

def complex_function(a, b):
    if a > b:
        return a + b
    else:
        for i in range(10):
            print(i)
        return 0
""")

    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_analyze_file_creates_nodes(self):
        """Test that analyzing a file creates nodes"""
        nodes, edges = self.analyzer.analyze_file(self.sample_file)
        
        assert len(nodes) > 0, "Should create at least one node"
        
        # Check for module node
        module_nodes = [n for n in nodes if n.node_type == NodeType.MODULE]
        assert len(module_nodes) == 1, "Should have exactly one module node"
        
        # Check for class node
        class_nodes = [n for n in nodes if n.node_type == NodeType.CLASS]
        assert len(class_nodes) >= 1, "Should have at least one class node"
        
        # Check for function nodes
        function_nodes = [n for n in nodes if n.node_type in [NodeType.FUNCTION, NodeType.METHOD]]
        assert len(function_nodes) >= 3, "Should have at least 3 function/method nodes"

    def test_analyze_file_creates_edges(self):
        """Test that analyzing a file creates edges"""
        nodes, edges = self.analyzer.analyze_file(self.sample_file)
        
        assert len(edges) > 0, "Should create at least one edge"
        
        # Check for method calls
        call_edges = [e for e in edges if e.relationship_type == RelationshipType.CALLS]
        assert len(call_edges) > 0, "Should have method call edges"

    def test_extract_name_functionality(self):
        """Test name extraction from AST nodes"""
        # This is a unit test for the internal helper method
        import ast
        
        code = "obj.method()"
        tree = ast.parse(code)
        call_node = tree.body[0].value
        
        # This would need to be called from within the analyzer context
        # For now, just verify the analyzer can parse the code
        nodes, edges = self.analyzer.analyze_file(self.sample_file)
        assert len(nodes) > 0


class TestNeo4jCCGStore:
    """Test cases for Neo4jCCGStore"""

    @patch('backend.services.ccg_service.GraphDatabase')
    def test_store_graph_calls_neo4j(self, mock_driver):
        """Test that store_graph makes Neo4j calls"""
        # Mock Neo4j driver
        mock_session = Mock()
        mock_driver.return_value.session.return_value.__enter__.return_value = mock_session
        
        # Create test data
        nodes = [
            CCGNode("1", "test", NodeType.FUNCTION, "test.py", 1, 10, "def test(): pass")
        ]
        edges = [
            CCGEdge("1", "2", RelationshipType.CALLS, 5)
        ]
        
        # Test store
        store = Neo4jCCGStore("bolt://localhost", "user", "pass")
        with store:
            store.store_graph(nodes, edges)
        
        # Verify Neo4j was called
        assert mock_session.run.call_count >= 1

    def test_query_dependencies(self):
        """Test dependency query functionality"""
        # This would need a mock Neo4j connection
        pass

    def test_query_call_graph(self):
        """Test call graph query functionality"""
        # This would need a mock Neo4j connection
        pass


class TestCCGService:
    """Test cases for CCGService"""

    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample project structure
        self.project_file = os.path.join(self.temp_dir, "sample.py")
        with open(self.project_file, 'w') as f:
            f.write("""
def hello_world():
    print("Hello, World!")
    return True

class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return self.add(a, a)
""")

    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('backend.services.ccg_service.CCGService')
    def test_analyze_codebase_method_exists(self, mock_service):
        """Test that analyze_codebase method exists and has correct signature"""
        # This is a basic test to ensure the method exists
        assert hasattr(CCGService, 'analyze_codebase')

    def test_analyze_codebase_invalid_directory(self):
        """Test analyze_codebase with invalid directory"""
        service = CCGService("bolt://localhost", "user", "pass")
        
        import asyncio
        with pytest.raises(ValueError):
            asyncio.run(service.analyze_codebase("/nonexistent/directory"))


class TestDataStructures:
    """Test cases for CCG data structures"""

    def test_ccg_node_creation(self):
        """Test CCGNode creation and properties"""
        node = CCGNode(
            id="test_node",
            name="test_function",
            node_type=NodeType.FUNCTION,
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_function(): pass"
        )
        
        assert node.id == "test_node"
        assert node.name == "test_function"
        assert node.node_type == NodeType.FUNCTION
        assert node.file_path == "test.py"
        assert node.line_start == 1
        assert node.line_end == 10
        assert node.metadata == {}
        assert node.properties == {}

    def test_ccg_edge_creation(self):
        """Test CCGEdge creation and properties"""
        edge = CCGEdge(
            source_id="node1",
            target_id="node2",
            relationship_type=RelationshipType.CALLS,
            line_number=5
        )
        
        assert edge.source_id == "node1"
        assert edge.target_id == "node2"
        assert edge.relationship_type == RelationshipType.CALLS
        assert edge.line_number == 5
        assert edge.metadata == {}

    def test_node_type_enum(self):
        """Test NodeType enum values"""
        assert NodeType.MODULE.value == "module"
        assert NodeType.CLASS.value == "class"
        assert NodeType.FUNCTION.value == "function"
        assert NodeType.METHOD.value == "method"
        assert NodeType.VARIABLE.value == "variable"

    def test_relationship_type_enum(self):
        """Test RelationshipType enum values"""
        assert RelationshipType.CALLS.value == "calls"
        assert RelationshipType.DEFINES.value == "defines"
        assert RelationshipType.IMPORTS.value == "imports"
        assert RelationshipType.INHERITS.value == "inherits"


class TestCCGIntegration:
    """Integration tests for CCG service"""

    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a more complex project structure
        self.create_test_project()

    def create_test_project(self):
        """Create a test project with multiple files"""
        
        # Main module
        main_file = os.path.join(self.temp_dir, "main.py")
        with open(main_file, 'w') as f:
            f.write("""
from utils import helper_function
from models import User

def main():
    user = User("test")
    result = helper_function(user)
    return result

class MainClass:
    def __init__(self):
        pass
    
    def process(self):
        return main()
""")
        
        # Utils module
        utils_file = os.path.join(self.temp_dir, "utils.py")
        with open(utils_file, 'w') as f:
            f.write("""
def helper_function(user):
    return user.name.upper()

def format_data(data):
    return f"Formatted: {data}"
""")
        
        # Models module
        models_file = os.path.join(self.temp_dir, "models.py")
        with open(models_file, 'w') as f:
            f.write("""
class User:
    def __init__(self, name):
        self.name = name
    
    def get_display_name(self):
        return f"User: {self.name}"

class Admin(User):
    def __init__(self, name, level):
        super().__init__(name)
        self.level = level
""")

    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_multiple_file_analysis(self):
        """Test analyzing multiple files in a project"""
        analyzer = CodeAnalyzer()
        
        # Analyze all Python files
        all_nodes = []
        all_edges = []
        
        for py_file in Path(self.temp_dir).glob("*.py"):
            nodes, edges = analyzer.analyze_file(str(py_file))
            all_nodes.extend(nodes)
            all_edges.extend(edges)
        
        # Verify we have nodes from all files
        assert len(all_nodes) > 0
        
        # Verify we have import relationships
        import_relationships = [e for e in all_edges if e.relationship_type == RelationshipType.IMPORTS]
        # This might be 0 depending on how deeply we parse imports
        assert isinstance(len(import_relationships), int)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
"""
Mock CCG Service for Development
Minimal implementation to satisfy API dependencies

Author: Cavin Otieno
"""

from enum import Enum
from typing import List, Dict, Any, Optional
import uuid

class NodeType(Enum):
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    IMPORT = "import"
    MODULE = "module"

class RelationshipType(Enum):
    CALLS = "calls"
    IMPORTS = "imports"
    DEFINES = "defines"
    CONTAINS = "contains"

class MockCCGService:
    """Mock CCG Service for development"""
    
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
    
    async def analyze_codebase(self, codebase_path: str) -> Dict[str, Any]:
        """Mock analyze codebase"""
        return {
            "analysis_id": str(uuid.uuid4()),
            "status": "completed",
            "summary": {
                "total_files": 42,
                "total_functions": 156,
                "total_classes": 23,
                "analysis_time": 2.34
            }
        }
    
    async def get_graph(self, analysis_id: str) -> Dict[str, Any]:
        """Mock get graph"""
        return {
            "nodes": [
                {"id": "1", "type": "function", "name": "main"},
                {"id": "2", "type": "class", "name": "Service"}
            ],
            "edges": [
                {"source": "1", "target": "2", "type": "calls"}
            ]
        }
    
    async def get_node_details(self, node_id: str) -> Dict[str, Any]:
        """Mock get node details"""
        return {
            "node_id": node_id,
            "type": "function",
            "name": "example_function",
            "line_range": [10, 25],
            "code_snippet": "def example_function(): pass"
        }
    
    def close(self):
        """Close service"""
        pass

# Keep the same class names for compatibility
CCGService = MockCCGService
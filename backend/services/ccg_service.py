"""
Code Context Graph (CCG) Service
Implements AST parsing and graph generation for deep code understanding.
Author: Cavin Otieno
"""

import ast
import json
from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from pathlib import Path
from neo4j import GraphDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class NodeType(Enum):
    """Node types in the Code Context Graph"""
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    IMPORT = "import"
    PARAMETER = "parameter"
    DECORATOR = "decorator"
    COMMENT = "comment"
    DOCSTRING = "docstring"


class RelationshipType(Enum):
    """Relationship types in the Code Context Graph"""
    CALLS = "calls"
    DEFINES = "defines"
    IMPORTS = "imports"
    INHERITS = "inherits"
    OVERRIDES = "overrides"
    USES = "uses"
    RETURNS = "returns"
    PARAMETER_OF = "parameter_of"
    DECORATED_BY = "decorated_by"
    CONTAINS = "contains"


@dataclass
class CCGNode:
    """Code Context Graph Node"""
    id: str
    name: str
    node_type: NodeType
    file_path: str
    line_start: int
    line_end: int
    content: str
    metadata: Dict[str, Any] = None
    properties: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.properties is None:
            self.properties = {}


@dataclass
class CCGEdge:
    """Code Context Graph Edge"""
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    line_number: int
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class CodeAnalyzer:
    """AST-based code analyzer for generating CCG nodes and edges"""

    def __init__(self):
        self.nodes: List[CCGNode] = []
        self.edges: List[CCGEdge] = []
        self.module_imports: Dict[str, Set[str]] = {}
        self.function_calls: List[Tuple[str, str, int]] = []  # (caller, callee, line)

    def analyze_file(self, file_path: str) -> Tuple[List[CCGNode], List[CCGEdge]]:
        """Analyze a Python file and generate CCG"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=file_path)
            self._analyze_module(tree, file_path, content)
            return self.nodes, self.edges

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return [], []

    def _analyze_module(self, tree: ast.AST, file_path: str, content: str):
        """Analyze module-level elements"""
        module_node = CCGNode(
            id=f"module:{file_path}",
            name=Path(file_path).stem,
            node_type=NodeType.MODULE,
            file_path=file_path,
            line_start=1,
            line_end=len(content.splitlines()),
            content=content,
            metadata={
                'total_lines': len(content.splitlines()),
                'total_classes': 0,
                'total_functions': 0,
                'total_variables': 0
            }
        )
        self.nodes.append(module_node)

        # Analyze top-level elements
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class(node, file_path, module_node.id)
            elif isinstance(node, ast.FunctionDef):
                self._analyze_function(node, file_path, module_node.id)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                self._analyze_variable(node, file_path, module_node.id)

    def _analyze_class(self, node: ast.ClassDef, file_path: str, parent_id: str):
        """Analyze class definition and methods"""
        class_id = f"class:{file_path}:{node.name}:{node.lineno}"
        
        # Create class node
        class_node = CCGNode(
            id=class_id,
            name=node.name,
            node_type=NodeType.CLASS,
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            content=ast.unparse(node),
            metadata={
                'base_classes': [ast.unparse(base) for base in node.bases],
                'decorators': [ast.unparse(dec) for dec in node.decorator_list],
                'docstring': ast.get_docstring(node)
            }
        )
        self.nodes.append(class_node)

        # Create inheritance relationships
        for base in node.bases:
            base_name = self._extract_name(base)
            if base_name:
                base_id = f"class::{base_name}"  # Simplified lookup
                edge = CCGEdge(
                    source_id=class_id,
                    target_id=base_id,
                    relationship_type=RelationshipType.INHERITS,
                    line_number=node.lineno
                )
                self.edges.append(edge)

        # Analyze class methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_id = f"method:{file_path}:{item.name}:{item.lineno}"
                method_node = CCGNode(
                    id=method_id,
                    name=item.name,
                    node_type=NodeType.METHOD,
                    file_path=file_path,
                    line_start=item.lineno,
                    line_end=item.end_lineno or item.lineno,
                    content=ast.unparse(item),
                    metadata={'class_name': node.name}
                )
                self.nodes.append(method_node)

                # Method -> Class relationship
                edge = CCGEdge(
                    source_id=method_id,
                    target_id=class_id,
                    relationship_type=RelationshipType.DEFINES,
                    line_number=item.lineno
                )
                self.edges.append(edge)

                # Analyze method internals
                self._analyze_function_calls(item, file_path, method_id)

    def _analyze_function(self, node: ast.FunctionDef, file_path: str, parent_id: str):
        """Analyze function definition and calls"""
        function_id = f"function:{file_path}:{node.name}:{node.lineno}"
        
        function_node = CCGNode(
            id=function_id,
            name=node.name,
            node_type=NodeType.FUNCTION,
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            content=ast.unparse(node),
            metadata={
                'args': [arg.arg for arg in node.args.args],
                'decorators': [ast.unparse(dec) for dec in node.decorator_list],
                'docstring': ast.get_docstring(node)
            }
        )
        self.nodes.append(function_node)

        # Function -> Parent relationship
        edge = CCGEdge(
            source_id=function_id,
            target_id=parent_id,
            relationship_type=RelationshipType.DEFINES,
            line_number=node.lineno
        )
        self.edges.append(edge)

        # Analyze function internals
        self._analyze_function_calls(node, file_path, function_id)

    def _analyze_function_calls(self, node: ast.FunctionDef, file_path: str, parent_id: str):
        """Analyze function calls within a function/method"""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                self._analyze_function_call(child, file_path, parent_id)

    def _analyze_function_call(self, node: ast.Call, file_path: str, parent_id: str):
        """Analyze a function call"""
        try:
            called_name = self._extract_call_name(node)
            if called_name:
                call_id = f"call:{file_path}:{called_name}:{node.lineno}"
                
                # Create call relationship
                edge = CCGEdge(
                    source_id=parent_id,
                    target_id=called_name,  # Could be more sophisticated mapping
                    relationship_type=RelationshipType.CALLS,
                    line_number=node.lineno,
                    metadata={
                        'call_site': ast.unparse(node),
                        'args_count': len(node.args),
                        'kwargs_count': len(node.keywords)
                    }
                )
                self.edges.append(edge)

                self.function_calls.append((parent_id, called_name, node.lineno))

        except Exception as e:
            logger.warning(f"Error analyzing function call at line {node.lineno}: {e}")

    def _analyze_variable(self, node: ast.Assign, file_path: str, parent_id: str):
        """Analyze variable assignments"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_id = f"variable:{file_path}:{target.id}:{node.lineno}"
                
                var_node = CCGNode(
                    id=var_id,
                    name=target.id,
                    node_type=NodeType.VARIABLE,
                    file_path=file_path,
                    line_start=node.lineno,
                    line_end=node.lineno,
                    content=ast.unparse(node),
                    metadata={
                        'value_type': ast.unparse(node.value),
                        'is_global': False
                    }
                )
                self.nodes.append(var_node)

                # Variable -> Parent relationship
                edge = CCGEdge(
                    source_id=var_id,
                    target_id=parent_id,
                    relationship_type=RelationshipType.USES,
                    line_number=node.lineno
                )
                self.edges.append(edge)

    def _extract_name(self, node: ast.AST) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return self._extract_name(node.value) + '.' + node.attr
        return ""

    def _extract_call_name(self, node: ast.Call) -> str:
        """Extract function call name"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return self._extract_name(node.func)
        return ""


class Neo4jCCGStore:
    """Neo4j-based storage for Code Context Graph"""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    def store_graph(self, nodes: List[CCGNode], edges: List[CCGEdge]):
        """Store CCG in Neo4j database"""
        with self.driver.session() as session:
            # Clear existing data for fresh analysis
            session.run("MATCH (n) DETACH DELETE n")
            
            # Create nodes
            for node in nodes:
                query = """
                CREATE (n:CodeNode {
                    id: $id,
                    name: $name,
                    node_type: $node_type,
                    file_path: $file_path,
                    line_start: $line_start,
                    line_end: $line_end,
                    content: $content,
                    metadata: $metadata,
                    properties: $properties
                })
                """
                session.run(query, {
                    'id': node.id,
                    'name': node.name,
                    'node_type': node.node_type.value,
                    'file_path': node.file_path,
                    'line_start': node.line_start,
                    'line_end': node.line_end,
                    'content': node.content,
                    'metadata': json.dumps(node.metadata),
                    'properties': json.dumps(node.properties)
                })

            # Create relationships
            for edge in edges:
                query = f"""
                MATCH (source {{id: $source_id}})
                MATCH (target {{id: $target_id}})
                CREATE (source)-[r:{edge.relationship_type.value} {{
                    line_number: $line_number,
                    metadata: $metadata
                }}]->(target)
                """
                session.run(query, {
                    'source_id': edge.source_id,
                    'target_id': edge.target_id,
                    'line_number': edge.line_number,
                    'metadata': json.dumps(edge.metadata)
                })

    def query_dependencies(self, file_path: str) -> List[Dict]:
        """Query file dependencies"""
        with self.driver.session() as session:
            query = """
            MATCH (n:CodeNode {file_path: $file_path})
            MATCH (n)-[r]->(m:CodeNode)
            RETURN m.file_path as dependent_file, 
                   type(r) as relationship,
                   r.metadata as metadata
            ORDER BY m.file_path
            """
            result = session.run(query, file_path=file_path)
            return [dict(record) for record in result]

    def query_call_graph(self, function_name: str) -> List[Dict]:
        """Query call graph for a function"""
        with self.driver.session() as session:
            query = """
            MATCH (caller:CodeNode {name: $function_name, node_type: 'function'})
            MATCH (caller)-[r:calls]->(callee:CodeNode)
            RETURN callee.name as called_function,
                   callee.node_type as node_type,
                   callee.file_path as file_path,
                   r.line_number as line_number,
                   r.metadata as metadata
            ORDER BY r.line_number
            """
            result = session.run(query, function_name=function_name)
            return [dict(record) for record in result]

    def query_class_hierarchy(self) -> List[Dict]:
        """Query class inheritance hierarchy"""
        with self.driver.session() as session:
            query = """
            MATCH (child:CodeNode {node_type: 'class'})
            MATCH (child)-[r:inherits]->(parent:CodeNode)
            RETURN child.name as child_class,
                   parent.name as parent_class,
                   child.file_path as file_path,
                   r.metadata as metadata
            ORDER BY child.name
            """
            result = session.run(query)
            return [dict(record) for record in result]

    def get_metrics(self) -> Dict[str, Any]:
        """Get CCG metrics"""
        with self.driver.session() as session:
            # Total nodes
            total_nodes = session.run("MATCH (n:CodeNode) RETURN count(n) as count").single()['count']
            
            # Total relationships
            total_edges = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']
            
            # Node types distribution
            node_types = session.run("""
                MATCH (n:CodeNode)
                RETURN n.node_type as node_type, count(n) as count
                ORDER BY count DESC
            """).values()
            
            # Files analyzed
            files_analyzed = session.run("""
                MATCH (n:CodeNode)
                RETURN DISTINCT n.file_path as file_path
                ORDER BY file_path
            """).values()
            
            return {
                'total_nodes': total_nodes,
                'total_edges': total_edges,
                'node_types': dict(node_types),
                'files_analyzed': len(files_analyzed),
                'file_list': [f[0] for f in files_analyzed]
            }


class CCGService:
    """Main CCG Service orchestrator"""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.analyzer = CodeAnalyzer()
        self.neo4j_store = Neo4jCCGStore(neo4j_uri, neo4j_user, neo4j_password)

    async def analyze_codebase(self, source_directory: str) -> Dict[str, Any]:
        """Analyze entire codebase and generate CCG"""
        source_path = Path(source_directory)
        if not source_path.exists():
            raise ValueError(f"Source directory {source_directory} does not exist")

        all_nodes = []
        all_edges = []
        files_processed = []

        # Find all Python files
        python_files = list(source_path.rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files to analyze")

        for file_path in python_files:
            try:
                relative_path = file_path.relative_to(source_path)
                logger.info(f"Analyzing: {relative_path}")
                
                nodes, edges = self.analyzer.analyze_file(str(file_path))
                all_nodes.extend(nodes)
                all_edges.extend(edges)
                files_processed.append(str(relative_path))

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                continue

        # Store in Neo4j
        with self.neo4j_store:
            self.neo4j_store.store_graph(all_nodes, all_edges)
            metrics = self.neo4j_store.get_metrics()

        result = {
            'files_processed': files_processed,
            'nodes_count': len(all_nodes),
            'edges_count': len(all_edges),
            'metrics': metrics,
            'analysis_timestamp': ast.literal_eval(json.dumps(asdict(
                CCGNode("timestamp", "analysis", NodeType.MODULE, "", 0, 0, "", 
                       {'timestamp': '2025-11-20T15:42:52Z'})
            ))
        }

        return result

    async def query_dependencies(self, file_path: str) -> List[Dict]:
        """Get file dependencies"""
        with self.neo4j_store:
            return self.neo4j_store.query_dependencies(file_path)

    async def query_call_graph(self, function_name: str) -> List[Dict]:
        """Get call graph for function"""
        with self.neo4j_store:
            return self.neo4j_store.query_call_graph(function_name)

    async def query_class_hierarchy(self) -> List[Dict]:
        """Get class inheritance hierarchy"""
        with self.neo4j_store:
            return self.neo4j_store.query_class_hierarchy()

    async def get_analysis_metrics(self) -> Dict[str, Any]:
        """Get CCG analysis metrics"""
        with self.neo4j_store:
            return self.neo4j_store.get_metrics()
"""
CCG (Code Context Graph) API Routes
Author: Cavin Otieno
"""

import os
import asyncio
from typing import List, Dict, Any
from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from pydantic import BaseModel, Field
import logging

from ..services.ccg_service import CCGService, NodeType, RelationshipType

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/ccg", tags=["Code Context Graph"])


class AnalyzeCodebaseRequest(BaseModel):
    """Request model for codebase analysis"""
    source_directory: str = Field(..., description="Path to the source code directory")
    file_patterns: List[str] = Field(default=["*.py"], description="File patterns to analyze")


class DependencyQuery(BaseModel):
    """Query model for dependencies"""
    file_path: str = Field(..., description="Relative path to the file")


class CallGraphQuery(BaseModel):
    """Query model for call graph"""
    function_name: str = Field(..., description="Name of the function to analyze")


class CCGAnalysisResponse(BaseModel):
    """Response model for CCG analysis"""
    success: bool
    message: str
    files_processed: List[str]
    nodes_count: int
    edges_count: int
    metrics: Dict[str, Any]
    analysis_timestamp: str


class DependencyResponse(BaseModel):
    """Response model for dependency queries"""
    success: bool
    dependencies: List[Dict[str, Any]]


class CallGraphResponse(BaseModel):
    """Response model for call graph queries"""
    success: bool
    call_graph: List[Dict[str, Any]]


class ClassHierarchyResponse(BaseModel):
    """Response model for class hierarchy"""
    success: bool
    hierarchy: List[Dict[str, Any]]


class CCGMetricsResponse(BaseModel):
    """Response model for CCG metrics"""
    success: bool
    metrics: Dict[str, Any]


# Dependency to get CCG service
def get_ccg_service():
    """Dependency to get CCG service instance"""
    from ..core.config import settings
    return CCGService(
        neo4j_uri=settings.NEO4J_URI,
        neo4j_user=settings.NEO4J_USER,
        neo4j_password=settings.NEO4J_PASSWORD
    )


@router.post("/analyze", response_model=CCGAnalysisResponse)
async def analyze_codebase(
    request: AnalyzeCodebaseRequest,
    background_tasks: BackgroundTasks,
    ccg_service: CCGService = Depends(get_ccg_service)
):
    """
    Analyze codebase and generate Code Context Graph
    
    This endpoint:
    1. Scans source directory for Python files
    2. Performs AST parsing and analysis
    3. Generates nodes and edges for the graph
    4. Stores results in Neo4j database
    5. Returns analysis metrics and file count
    """
    try:
        # Validate source directory
        source_path = Path(request.source_directory)
        if not source_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Source directory does not exist: {request.source_directory}"
            )
        
        if not source_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Path is not a directory: {request.source_directory}"
            )
        
        # Run analysis
        logger.info(f"Starting CCG analysis for directory: {request.source_directory}")
        result = await ccg_service.analyze_codebase(request.source_directory)
        
        return CCGAnalysisResponse(
            success=True,
            message="Code analysis completed successfully",
            files_processed=result["files_processed"],
            nodes_count=result["nodes_count"],
            edges_count=result["edges_count"],
            metrics=result["metrics"],
            analysis_timestamp=result["analysis_timestamp"]
        )
        
    except Exception as e:
        logger.error(f"Error analyzing codebase: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze codebase: {str(e)}"
        )


@router.get("/dependencies", response_model=DependencyResponse)
async def get_dependencies(
    file_path: str = Query(..., description="Relative path to the file"),
    ccg_service: CCGService = Depends(get_ccg_service)
):
    """
    Get dependencies for a specific file
    
    Returns a list of files that depend on the specified file
    and the relationship types between them.
    """
    try:
        dependencies = await ccg_service.query_dependencies(file_path)
        
        return DependencyResponse(
            success=True,
            dependencies=dependencies
        )
        
    except Exception as e:
        logger.error(f"Error querying dependencies for {file_path}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query dependencies: {str(e)}"
        )


@router.get("/call-graph", response_model=CallGraphResponse)
async def get_call_graph(
    function_name: str = Query(..., description="Name of the function to analyze"),
    ccg_service: CCGService = Depends(get_ccg_service)
):
    """
    Get call graph for a specific function
    
    Returns all functions called by the specified function
    and their relationship metadata.
    """
    try:
        call_graph = await ccg_service.query_call_graph(function_name)
        
        return CallGraphResponse(
            success=True,
            call_graph=call_graph
        )
        
    except Exception as e:
        logger.error(f"Error querying call graph for {function_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query call graph: {str(e)}"
        )


@router.get("/class-hierarchy", response_model=ClassHierarchyResponse)
async def get_class_hierarchy(
    ccg_service: CCGService = Depends(get_ccg_service)
):
    """
    Get class inheritance hierarchy
    
    Returns all class inheritance relationships in the analyzed codebase.
    """
    try:
        hierarchy = await ccg_service.query_class_hierarchy()
        
        return ClassHierarchyResponse(
            success=True,
            hierarchy=hierarchy
        )
        
    except Exception as e:
        logger.error(f"Error querying class hierarchy: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query class hierarchy: {str(e)}"
        )


@router.get("/metrics", response_model=CCGMetricsResponse)
async def get_ccg_metrics(
    ccg_service: CCGService = Depends(get_ccg_service)
):
    """
    Get CCG analysis metrics
    
    Returns overall statistics about the analyzed codebase including
    node counts, relationship counts, and distribution metrics.
    """
    try:
        metrics = await ccg_service.get_analysis_metrics()
        
        return CCGMetricsResponse(
            success=True,
            metrics=metrics
        )
        
    except Exception as e:
        logger.error(f"Error getting CCG metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get metrics: {str(e)}"
        )


@router.get("/health")
async def ccg_health_check():
    """Health check endpoint for CCG service"""
    try:
        from ..core.config import settings
        
        # Check if Neo4j connection is available
        ccg_service = CCGService(
            neo4j_uri=settings.NEO4J_URI,
            neo4j_user=settings.NEO4J_USER,
            neo4j_password=settings.NEO4J_PASSWORD
        )
        
        with ccg_service.neo4j_store:
            # Simple test query
            ccg_service.neo4j_store.get_metrics()
        
        return {
            "status": "healthy",
            "service": "Code Context Graph",
            "database": "Neo4j",
            "timestamp": "2025-11-20T15:42:52Z"
        }
        
    except Exception as e:
        logger.error(f"CCG health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"CCG service is unhealthy: {str(e)}"
        )


@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats for CCG analysis"""
    return {
        "supported_formats": ["*.py"],
        "description": "Currently supports Python source files (.py)",
        "max_file_size": "10MB",
        "max_files_per_analysis": 1000
    }
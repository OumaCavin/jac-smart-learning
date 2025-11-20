"""
CCG (Code Context Graph) API Routes
Author: Cavin Otieno
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/ccg", tags=["Code Context Graph"])


class AnalyzeCodeRequest(BaseModel):
    """Request model for analyzing a single code snippet"""
    code: str = Field(..., description="Source code to analyze")
    language: str = Field(default="python", description="Programming language")
    filename: str = Field(default="sample.py", description="Filename for analysis")


@router.post("/analyze")
async def analyze_code(request: AnalyzeCodeRequest):
    """Analyze a single code snippet"""
    try:
        logger.info(f"Analyzing code snippet in {request.language}")
        
        # Mock analysis result
        lines = request.code.split('\n')
        functions = [line.strip() for line in lines if line.strip().startswith('def ')]
        classes = [line.strip() for line in lines if line.strip().startswith('class ')]
        
        analysis_result = {
            "success": True,
            "message": "Code analysis completed successfully",
            "language": request.language,
            "filename": request.filename,
            "lines_count": len(lines),
            "characters_count": len(request.code),
            "functions_detected": len(functions),
            "classes_detected": len(classes),
            "complexity_score": min(len([line for line in lines if 'if ' in line or 'for ' in line or 'while ' in line]) * 10, 100),
            "analysis_timestamp": "2025-11-20T17:25:00Z",
            "functions": functions,
            "classes": classes
        }
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze code: {str(e)}"
        )


@router.get("/health")
async def ccg_health_check():
    """Health check endpoint for CCG service"""
    return {
        "status": "healthy",
        "service": "Code Context Graph",
        "version": "1.0.0",
        "timestamp": "2025-11-20T17:25:00Z"
    }


@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats for CCG analysis"""
    return {
        "supported_languages": ["python", "javascript", "typescript", "java"],
        "supported_extensions": ["py", "js", "ts", "java"],
        "max_file_size": "10MB",
        "max_files_per_analysis": 1000
    }

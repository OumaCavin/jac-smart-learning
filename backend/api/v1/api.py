"""
Main API Router for EMAS Backend
Combines all API route modules

Author: Cavin Otieno
"""

from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# Import existing routers with error handling
try:
    from .ccg import router as ccg_router
    api_router.include_router(ccg_router, prefix="/ccg")
except ImportError as e:
    print(f"Warning: Could not import CCG router: {e}")

try:
    from .quality import router as quality_router
    api_router.include_router(quality_router, prefix="/quality")
except ImportError as e:
    print(f"Warning: Could not import Quality router: {e}")

# Default routes
@api_router.get("/")
async def root():
    """Root API endpoint"""
    return {
        "message": "JAC Smart Learning API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "ccg": "/ccg",
            "quality": "/quality",
            "health": "/health"
        }
    }

@api_router.get("/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "endpoints_available": ["ccg", "quality"]
    }
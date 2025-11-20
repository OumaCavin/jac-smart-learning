"""
Enterprise Multi-Agent System (EMAS) Backend
Production-ready, scalable backend service for multi-agent orchestration

Author: Cavin Otieno
Contact: cavin.otieno012@gmail.com | +254708101604
LinkedIn: https://www.linkedin.com/in/cavin-otieno-9a841260/
"""

import os
import sys
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn

from backend.core.config import settings
from backend.core.database import init_db
from backend.core.websocket import setup_websocket_handler
from backend.api.v1.api import api_router
from backend.core.middleware import setup_middleware
from backend.core.security import setup_security
from backend.services.agent_registry import AgentRegistry
from backend.services.message_bus import MessageBus
from backend.services.quality_assessment import QualityAssessmentService
from backend.services.code_context_graph import CodeContextGraphService


# Global services (will be initialized in startup)
agent_registry: AgentRegistry = None
message_bus: MessageBus = None
quality_service: QualityAssessmentService = None
ccg_service: CodeContextGraphService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global agent_registry, message_bus, quality_service, ccg_service
    
    logger.info("🚀 Starting Enterprise Multi-Agent System Backend")
    
    try:
        # Initialize database
        logger.info("📊 Initializing database connections...")
        await init_db()
        
        # Initialize services
        logger.info("🤖 Initializing agent registry...")
        agent_registry = AgentRegistry()
        
        logger.info("📡 Initializing message bus...")
        message_bus = MessageBus()
        
        logger.info("🎯 Initializing quality assessment service...")
        quality_service = QualityAssessmentService()
        
        logger.info("🧠 Initializing code context graph service...")
        ccg_service = CodeContextGraphService()
        
        # Start services
        logger.info("🚀 Starting core services...")
        await agent_registry.start()
        await message_bus.start()
        
        # Register built-in agents
        logger.info("📝 Registering built-in agents...")
        await register_builtin_agents()
        
        logger.info("✅ Backend startup completed successfully!")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to start backend: {str(e)}")
        raise
    
    finally:
        logger.info("🔄 Shutting down backend services...")
        
        # Cleanup services
        if message_bus:
            await message_bus.stop()
        if agent_registry:
            await agent_registry.stop()
        
        logger.info("✅ Backend shutdown completed")


async def register_builtin_agents():
    """Register built-in agent types"""
    from backend.agents.code_analysis import CodeAnalysisAgent
    from backend.agents.test_generation import TestGenerationAgent
    from backend.agents.security_scanning import SecurityScanningAgent
    from backend.agents.performance_analysis import PerformanceAnalysisAgent
    from backend.agents.documentation import DocumentationAgent
    
    agents = [
        CodeAnalysisAgent(),
        TestGenerationAgent(),
        SecurityScanningAgent(),
        PerformanceAnalysisAgent(),
        DocumentationAgent()
    ]
    
    for agent in agents:
        await agent_registry.register_agent(agent)


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    Enterprise Multi-Agent System (EMAS) Backend
    
    A production-ready, scalable platform for orchestrating multiple intelligent agents 
    to solve complex problems. Features real-time updates, code analysis, and quality assessment.
    
    ## Key Features
    
    - 🤖 **Multi-Agent Orchestration**: Advanced coordination system with Chain of Responsibility pattern
    - ⚡ **Real-Time Updates**: WebSocket-based live progress tracking
    - 🧠 **Code Context Graph**: Deep code understanding through AST analysis
    - 🎯 **Quality Assessment**: Multi-dimensional code evaluation
    - 📊 **Scalable Architecture**: Microservices design with Kubernetes support
    - 🔒 **Enterprise Security**: Comprehensive auth and secrets management
    
    ## Architecture
    
    Built with modern technologies:
    - **FastAPI** for high-performance REST APIs
    - **WebSockets** for real-time communication
    - **PostgreSQL** for persistent data storage
    - **Redis** for caching and session management
    - **NATS** for message queuing and inter-service communication
    - **Neo4j** for graph database operations
    - **Prometheus & Grafana** for monitoring and observability
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Global request counter for metrics
request_count = 0


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Add basic metrics middleware"""
    global request_count
    request_count += 1
    
    start_time = asyncio.get_event_loop().time()
    
    try:
        response = await call_next(request)
        
        # Calculate request duration
        duration = asyncio.get_event_loop().time() - start_time
        
        # Log request metrics
        logger.info(
            f"Request {request_count}: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Duration: {duration:.3f}s"
        )
        
        # Add response headers
        response.headers["X-Request-ID"] = str(request_count)
        response.headers["X-Response-Time"] = f"{duration:.3f}"
        
        return response
        
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Enterprise Multi-Agent System (EMAS) Backend",
        "version": settings.APP_VERSION,
        "author": "Cavin Otieno",
        "contact": "cavin.otieno012@gmail.com",
        "documentation": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global agent_registry, message_bus, quality_service, ccg_service
    
    try:
        # Check database connectivity
        from backend.core.database import get_db_session
        async with get_db_session() as db:
            await db.execute("SELECT 1")
        
        # Check Redis connectivity
        from backend.core.database import redis_client
        await redis_client.ping()
        
        # Check service status
        services_status = {
            "database": "healthy",
            "redis": "healthy",
            "agent_registry": await agent_registry.health_check() if agent_registry else "not_initialized",
            "message_bus": await message_bus.health_check() if message_bus else "not_initialized",
            "quality_service": await quality_service.health_check() if quality_service else "not_initialized",
            "ccg_service": await ccg_service.health_check() if ccg_service else "not_initialized"
        }
        
        # Check if all services are healthy
        all_healthy = all(status == "healthy" for status in services_status.values())
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "timestamp": asyncio.get_event_loop().time(),
            "services": services_status,
            "version": settings.APP_VERSION
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": asyncio.get_event_loop().time()
        }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
    except Exception as e:
        logger.error(f"Metrics endpoint error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Metrics unavailable"}
        )


# Setup middleware
setup_middleware(app)

# Setup security
setup_security(app)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Setup WebSocket handler
setup_websocket_handler(app)

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "backend.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
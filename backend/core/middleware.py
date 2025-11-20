"""
Middleware Configuration for EMAS Backend
Minimal implementation for development

Author: Cavin Otieno
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from loguru import logger

def setup_middleware(app: FastAPI):
    """Setup application middleware"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware (if needed)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.local"]
    )
    
    logger.info("🔧 Middleware configured")
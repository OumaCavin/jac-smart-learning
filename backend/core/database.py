"""
Simplified Database Configuration for Development Mode
Minimal implementation to allow FastAPI server to start without external dependencies

Author: Cavin Otieno
"""

import asyncio
from typing import AsyncGenerator
from contextlib import asynccontextmanager

# Mock objects for development
class MockAsyncSession:
    """Mock async session for development"""
    
    async def execute(self, query):
        """Mock execute method"""
        return self
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

# Global variables
async_engine = None
session_maker = None
redis_client = None
database_pool = None

async def init_db():
    """Initialize database connections"""
    global async_engine, session_maker, redis_client, database_pool
    
    print("📊 Initializing mock database connections...")
    
    # Mock Redis connection
    redis_client = MockRedis()
    
    # Create mock session maker
    session_maker = MockSessionMaker()

class MockRedis:
    """Mock Redis client"""
    
    async def ping(self):
        return True

class MockSessionMaker:
    """Mock session maker"""
    
    @asynccontextmanager
    async def get_db_session(self):
        """Get mock database session"""
        yield MockAsyncSession()

# Export mock session getter
@asynccontextmanager
async def get_db_session():
    """Get database session context manager"""
    async with session_maker.get_db_session() as session:
        yield session
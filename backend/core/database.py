"""
Database Configuration and Models for EMAS Backend
PostgreSQL with asyncpg and SQLAlchemy ORM

Author: Cavin Otieno
"""

import asyncio
from typing import AsyncGenerator
from contextlib import asynccontextmanager

import asyncpg
import redis.asyncio as redis
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import declarative_base

from backend.core.config import settings

# SQLAlchemy setup
Base = declarative_base()
metadata = MetaData()

# Database engine
engine = None
async_engine = None
session_maker = None

# Redis connection
redis_client = None

# Connection pool
database_pool = None


async def init_db():
    """Initialize database connections and create tables"""
    global engine, async_engine, session_maker, redis_client, database_pool
    
    try:
        # Create async database engine
        async_engine = create_async_engine(
            settings.get_database_url(),
            echo=settings.DEBUG_SQL,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_timeout=settings.DATABASE_POOL_TIMEOUT,
            pool_recycle=settings.DATABASE_POOL_RECYCLE,
            connect_args={
                "server_settings": {
                    "application_name": "EMAS Backend",
                    "jit": "off"  # Disable JIT for better connection performance
                }
            }
        )
        
        # Create session factory
        session_maker = async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create Redis connection
        redis_client = redis.from_url(
            settings.get_redis_url(),
            encoding="utf-8",
            decode_responses=True,
            socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
            socket_connect_timeout=5,
            max_connections=settings.REDIS_MAX_CONNECTIONS
        )
        
        # Test database connections
        await test_connections()
        
        # Create tables
        await create_tables()
        
        # Initialize connection pool
        database_pool = await create_connection_pool()
        
        print("✅ Database initialization completed successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        raise


async def test_connections():
    """Test database and Redis connections"""
    
    # Test PostgreSQL connection
    conn = await asyncpg.connect(settings.get_database_url())
    await conn.execute("SELECT 1")
    await conn.close()
    
    # Test Redis connection
    await redis_client.ping()
    
    print("✅ Database connections tested successfully")


async def create_connection_pool():
    """Create connection pool for performance"""
    pool = await asyncpg.create_pool(
        settings.get_database_url(),
        min_size=2,
        max_size=settings.DATABASE_POOL_SIZE,
        command_timeout=60
    )
    return pool


async def create_tables():
    """Create all database tables"""
    
    # Import all models to ensure they're registered
    from backend.models.user import User
    from backend.models.agent import Agent, AgentExecution, AgentTask
    from backend.models.project import Project, ProjectAnalysis
    from backend.models.code_analysis import CodeFile, CodeAnalysis, AnalysisResult
    from backend.models.quality_assessment import QualityMetric, QualityReport
    from backend.models.message import Message, MessageQueue
    
    async with async_engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections"""
    global async_engine, redis_client, database_pool
    
    try:
        if async_engine:
            await async_engine.dispose()
        
        if redis_client:
            await redis_client.close()
        
        if database_pool:
            await database_pool.close()
        
        print("✅ Database connections closed")
        
    except Exception as e:
        print(f"❌ Error closing database connections: {str(e)}")


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session with automatic cleanup"""
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI endpoints"""
    async with get_db_session() as session:
        yield session


async def get_redis() -> redis.Redis:
    """Get Redis client"""
    return redis_client


# Database models will be defined in separate files
# Here's a quick reference structure:

"""
Database Models Structure:

1. User Management
   - User (authentication and user data)
   - UserSession (session management)

2. Agent System
   - Agent (agent definitions and metadata)
   - AgentExecution (execution history and status)
   - AgentTask (individual tasks for agents)

3. Project Management
   - Project (project metadata and settings)
   - ProjectAnalysis (analysis results and history)

4. Code Analysis
   - CodeFile (file metadata and content references)
   - CodeAnalysis (analysis results and metrics)
   - AnalysisResult (detailed analysis data)

5. Quality Assessment
   - QualityMetric (individual quality metrics)
   - QualityReport (comprehensive quality reports)

6. Message System
   - Message (message content and metadata)
   - MessageQueue (queue management for agents)

7. Configuration
   - SystemConfig (system-wide configuration)
   - AgentConfig (agent-specific configuration)

8. Audit and Monitoring
   - AuditLog (audit trail for all operations)
   - PerformanceMetric (system performance data)
   - ErrorLog (error tracking and reporting)
"""

# Utility functions for database operations

async def execute_query(query: str, *args):
    """Execute a raw SQL query"""
    async with get_db_session() as session:
        result = await session.execute(query, args)
        return result


async def fetch_one(query: str, *args):
    """Fetch a single row from database"""
    async with get_db_session() as session:
        result = await session.execute(query, args)
        return result.fetchone()


async def fetch_all(query: str, *args):
    """Fetch multiple rows from database"""
    async with get_db_session() as session:
        result = await session.execute(query, args)
        return result.fetchall()


async def execute_transaction(queries):
    """Execute multiple queries in a transaction"""
    async with get_db_session() as session:
        try:
            results = []
            for query in queries:
                if isinstance(query, tuple):
                    result = await session.execute(query[0], query[1])
                else:
                    result = await session.execute(query)
                results.append(result)
            await session.commit()
            return results
        except Exception as e:
            await session.rollback()
            raise e


# Redis utilities

async def cache_get(key: str):
    """Get value from Redis cache"""
    return await redis_client.get(key)


async def cache_set(key: str, value: str, ttl: int = None):
    """Set value in Redis cache"""
    if ttl:
        await redis_client.setex(key, ttl, value)
    else:
        await redis_client.set(key, value)


async def cache_delete(key: str):
    """Delete value from Redis cache"""
    await redis_client.delete(key)


async def cache_increment(key: str, amount: int = 1):
    """Increment counter in Redis"""
    return await redis_client.incrby(key, amount)


async def cache_exists(key: str) -> bool:
    """Check if key exists in Redis"""
    return await redis_client.exists(key) > 0


async def cache_expire(key: str, seconds: int):
    """Set expiration for Redis key"""
    await redis_client.expire(key, seconds)


# Cache decorators

def cached(ttl: int = 300):
    """Decorator for caching function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = await cache_get(key)
            if cached_result:
                import json
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_set(key, result, ttl)
            
            return result
        return wrapper
    return decorator


# Performance monitoring

async def record_metric(name: str, value: float, tags: dict = None):
    """Record performance metrics to Redis for monitoring"""
    import time
    
    timestamp = int(time.time())
    metric_key = f"metrics:{name}:{timestamp}"
    
    metric_data = {
        "value": value,
        "timestamp": timestamp,
        "tags": tags or {}
    }
    
    import json
    await cache_set(metric_key, json.dumps(metric_data), ttl=3600 * 24)  # 24 hours


async def get_metrics(name: str, hours: int = 24):
    """Get performance metrics from Redis"""
    import time
    from datetime import datetime, timedelta
    
    end_time = int(time.time())
    start_time = int((datetime.now() - timedelta(hours=hours)).timestamp())
    
    metrics = []
    pattern = f"metrics:{name}:*"
    
    # Get all metric keys
    keys = await redis_client.keys(pattern)
    
    for key in keys:
        try:
            import json
            data = json.loads(await cache_get(key))
            timestamp = data.get("timestamp", 0)
            
            if start_time <= timestamp <= end_time:
                metrics.append(data)
        except (json.JSONDecodeError, TypeError):
            continue
    
    return sorted(metrics, key=lambda x: x.get("timestamp", 0))
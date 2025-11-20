"""
Configuration Management for Enterprise Multi-Agent System
Centralized configuration with environment variable support

Author: Cavin Otieno
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseSettings, validator, Field
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    
    # Application Settings
    APP_NAME: str = Field(default="Enterprise Multi-Agent System", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    APP_HOST: str = Field(default="0.0.0.0", env="APP_HOST")
    APP_PORT: int = Field(default=8000, env="APP_PORT")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://emas_user:secure_password_123@localhost:5432/emas_db",
        env="DATABASE_URL"
    )
    DATABASE_HOST: str = Field(default="localhost", env="DATABASE_HOST")
    DATABASE_PORT: int = Field(default=5432, env="DATABASE_PORT")
    DATABASE_NAME: str = Field(default="emas_db", env="DATABASE_NAME")
    DATABASE_USER: str = Field(default="emas_user", env="DATABASE_USER")
    DATABASE_PASSWORD: str = Field(default="secure_password_123", env="DATABASE_PASSWORD")
    
    # Database Connection Pool
    DATABASE_POOL_SIZE: int = Field(default=10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    DATABASE_POOL_RECYCLE: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    
    # Redis Configuration
    REDIS_URL: str = Field(
        default="redis://:redis_password_123@localhost:6379/0",
        env="REDIS_URL"
    )
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_PASSWORD: str = Field(default="redis_password_123", env="REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    REDIS_MAX_CONNECTIONS: int = Field(default=10, env="REDIS_MAX_CONNECTIONS")
    REDIS_SOCKET_TIMEOUT: int = Field(default=5, env="REDIS_SOCKET_TIMEOUT")
    
    # Message Bus Configuration
    NATS_URL: str = Field(default="nats://localhost:4222", env="NATS_URL")
    NATS_HOST: str = Field(default="localhost", env="NATS_HOST")
    NATS_PORT: int = Field(default=4222, env="NATS_PORT")
    NATS_USER: Optional[str] = Field(default=None, env="NATS_USER")
    NATS_PASSWORD: Optional[str] = Field(default=None, env="NATS_PASSWORD")
    NATS_CLUSTER_ID: str = Field(default="emas-cluster", env="NATS_CLUSTER_ID")
    NATS_CLIENT_ID: str = Field(default="emas-client", env="NATS_CLIENT_ID")
    NATS_JETSTREAM_ENABLED: bool = Field(default=True, env="NATS_JETSTREAM_ENABLED")
    NATS_JETSTREAM_SUBJECT_PREFIX: str = Field(default="emas", env="NATS_JETSTREAM_SUBJECT_PREFIX")
    
    # Authentication & Security
    JWT_SECRET: str = Field(
        default="your-super-secret-jwt-key-change-in-production-at-least-64-chars",
        env="JWT_SECRET"
    )
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # OAuth2 Configuration
    GITHUB_CLIENT_ID: Optional[str] = Field(default=None, env="GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: Optional[str] = Field(default=None, env="GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI: str = Field(default="http://localhost:3000/auth/github/callback", env="GITHUB_REDIRECT_URI")
    
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(default="http://localhost:3000/auth/google/callback", env="GOOGLE_REDIRECT_URI")
    
    # Password Hashing
    BCRYPT_ROUNDS: int = Field(default=12, env="BCRYPT_ROUNDS")
    PASSWORD_MIN_LENGTH: int = Field(default=8, env="PASSWORD_MIN_LENGTH")
    PASSWORD_REQUIRE_SPECIAL: bool = Field(default=True, env="PASSWORD_REQUIRE_SPECIAL")
    PASSWORD_REQUIRE_UPPERCASE: bool = Field(default=True, env="PASSWORD_REQUIRE_UPPERCASE")
    PASSWORD_REQUIRE_LOWERCASE: bool = Field(default=True, env="PASSWORD_REQUIRE_LOWERCASE")
    PASSWORD_REQUIRE_DIGITS: bool = Field(default=True, env="PASSWORD_REQUIRE_DIGITS")
    
    # Session Configuration
    SESSION_SECRET: str = Field(default="your-session-secret-key-change-in-production", env="SESSION_SECRET")
    SESSION_TIMEOUT: int = Field(default=3600, env="SESSION_TIMEOUT")
    
    # WebSocket Configuration
    WS_HOST: str = Field(default="0.0.0.0", env="WS_HOST")
    WS_PORT: int = Field(default=8001, env="WS_PORT")
    WS_PATH: str = Field(default="/ws", env="WS_PATH")
    WS_MAX_CONNECTIONS: int = Field(default=1000, env="WS_MAX_CONNECTIONS")
    WS_HEARTBEAT_INTERVAL: int = Field(default=30, env="WS_HEARTBEAT_INTERVAL")
    WS_HEARTBEAT_TIMEOUT: int = Field(default=10, env="WS_HEARTBEAT_TIMEOUT")
    
    # Graph Database (Neo4j)
        # Neo4j Configuration
    NEO4J_URI: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    NEO4J_USER: str = Field(default="neo4j", env="NEO4J_USERNAME")
    NEO4J_PASSWORD: str = Field(default="neo4j_password", env="NEO4J_PASSWORD")
    NEO4J_DATABASE: str = Field(default="emas_graph", env="NEO4J_DATABASE")
    
    # AI/LLM Integration
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    OPENAI_MAX_TOKENS: int = Field(default=2048, env="OPENAI_MAX_TOKENS")
    OPENAI_TEMPERATURE: float = Field(default=0.7, env="OPENAI_TEMPERATURE")
    
    # Supabase Configuration
    SUPABASE_URL: str = Field(
        default="https://rjgrobamzmbcvakwltxt.supabase.co",
        env="SUPABASE_URL"
    )
    SUPABASE_ANON_KEY: str = Field(
        default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqZ3JvYmFtem1iY3Zha3dsdHh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1ODc2ODQsImV4cCI6MjA3OTE2MzY4NH0.NH6i7UUor07PevpK7AMzMw7LvLP8j9wtuypfa_azip0",
        env="SUPABASE_ANON_KEY"
    )
    SUPABASE_SERVICE_ROLE: str = Field(
        default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqZ3JvYmFtem1iY3Zha3dsdHh0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzU4NzY4NCwiZXhwIjoyMDc5MTYzNjg0fQ.5m60ck3umars1l2_Yz-BOI5URajEZoDqELkcVglv2lA",
        env="SUPABASE_SERVICE_ROLE"
    )
    SUPABASE_DB_PASSWORD: str = Field(default="Airtel!23!23", env="SUPABASE_DB_PASSWORD")
    
    # Google AI/ML
    GOOGLE_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    GOOGLE_MAKERSUITE_URL: str = Field(
        default="https://generativelanguage.googleapis.com",
        env="GOOGLE_MAKERSUITE_URL"
    )
    
    # Monitoring & Observability
    PROMETHEUS_URL: str = Field(default="http://localhost:9090", env="PROMETHEUS_URL")
    PROMETHEUS_ENABLED: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    
    GRAFANA_URL: str = Field(default="http://localhost:3001", env="GRAFANA_URL")
    GRAFANA_ADMIN_USER: str = Field(default="admin", env="GRAFANA_ADMIN_USER")
    GRAFANA_ADMIN_PASSWORD: str = Field(default="admin123", env="GRAFANA_ADMIN_PASSWORD")
    
    JAEGER_URL: str = Field(default="http://localhost:16686", env="JAEGER_URL")
    JAEGER_ENABLED: bool = Field(default=True, env="JAEGER_ENABLED")
    JAEGER_SAMPLER_TYPE: str = Field(default="const", env="JAEGER_SAMPLER_TYPE")
    JAEGER_SAMPLER_PARAM: int = Field(default=1, env="JAEGER_SAMPLER_PARAM")
    
    LOKI_URL: str = Field(default="http://localhost:3100", env="LOKI_URL")
    LOKI_ENABLED: bool = Field(default=True, env="LOKI_ENABLED")
    
    # Security Vault
    VAULT_ADDR: str = Field(default="http://localhost:8200", env="VAULT_ADDR")
    VAULT_TOKEN: Optional[str] = Field(default=None, env="VAULT_TOKEN")
    VAULT_ROLE_ID: Optional[str] = Field(default=None, env="VAULT_ROLE_ID")
    VAULT_SECRET_ID: Optional[str] = Field(default=None, env="VAULT_SECRET_ID")
    
    # Email Configuration
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="cavin.otieno012@gmail.com", env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_USE_TLS: bool = Field(default=True, env="SMTP_USE_TLS")
    SMTP_USE_SSL: bool = Field(default=False, env="SMTP_USE_SSL")
    
    EMAIL_FROM_NAME: str = Field(default="EMAS System", env="EMAIL_FROM_NAME")
    EMAIL_FROM_ADDRESS: str = Field(default="cavin.otieno012@gmail.com", env="EMAIL_FROM_ADDRESS")
    EMAIL_REPLY_TO: str = Field(default="noreply@cavnotieno.com", env="EMAIL_REPLY_TO")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_UPLOAD_SIZE: int = Field(default=10485760, env="MAX_UPLOAD_SIZE")  # 10MB
    ALLOWED_EXTENSIONS: str = Field(
        default="py,js,ts,jsx,tsx,java,go,rs,rb,php,cpp,c,h,hpp",
        env="ALLOWED_EXTENSIONS"
    )
    
    # S3 Storage (Production)
    S3_BUCKET: Optional[str] = Field(default=None, env="S3_BUCKET")
    S3_REGION: str = Field(default="us-east-1", env="S3_REGION")
    S3_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="S3_ACCESS_KEY_ID")
    S3_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="S3_SECRET_ACCESS_KEY")
    S3_ENDPOINT_URL: Optional[str] = Field(default=None, env="S3_ENDPOINT_URL")
    
    # Agent Configuration
    AGENT_MAX_CONCURRENT: int = Field(default=50, env="AGENT_MAX_CONCURRENT")
    AGENT_TIMEOUT: int = Field(default=300, env="AGENT_TIMEOUT")  # 5 minutes
    AGENT_RETRY_ATTEMPTS: int = Field(default=3, env="AGENT_RETRY_ATTEMPTS")
    AGENT_RETRY_DELAY: int = Field(default=5, env="AGENT_RETRY_DELAY")
    AGENT_HEALTH_CHECK_INTERVAL: int = Field(default=30, env="AGENT_HEALTH_CHECK_INTERVAL")
    
    # Agent Types
    CODE_ANALYSIS_AGENT_ENABLED: bool = Field(default=True, env="CODE_ANALYSIS_AGENT_ENABLED")
    TEST_GENERATION_AGENT_ENABLED: bool = Field(default=True, env="TEST_GENERATION_AGENT_ENABLED")
    SECURITY_SCANNING_AGENT_ENABLED: bool = Field(default=True, env="SECURITY_SCANNING_AGENT_ENABLED")
    PERFORMANCE_ANALYSIS_AGENT_ENABLED: bool = Field(default=True, env="PERFORMANCE_ANALYSIS_AGENT_ENABLED")
    DOCUMENTATION_AGENT_ENABLED: bool = Field(default=True, env="DOCUMENTATION_AGENT_ENABLED")
    
    # Code Context Graph (CCG)
    CCG_MAX_NODES: int = Field(default=10000, env="CCG_MAX_NODES")
    CCG_MAX_EDGES: int = Field(default=50000, env="CCG_MAX_EDGES")
    CCG_CACHE_TTL: int = Field(default=3600, env="CCG_CACHE_TTL")
    CCG_ANALYSIS_TIMEOUT: int = Field(default=60, env="CCG_ANALYSIS_TIMEOUT")
    
    # AST Parsing
    SUPPORTED_LANGUAGES: str = Field(
        default="python,javascript,typescript,java,go,rust,php,cpp,c",
        env="SUPPORTED_LANGUAGES"
    )
    AST_PARSE_TIMEOUT: int = Field(default=30, env="AST_PARSE_TIMEOUT")
    
    # Quality Assessment Engine
    QA_CORRECTNESS_WEIGHT: float = Field(default=0.25, env="QA_CORRECTNESS_WEIGHT")
    QA_PERFORMANCE_WEIGHT: float = Field(default=0.20, env="QA_PERFORMANCE_WEIGHT")
    QA_SECURITY_WEIGHT: float = Field(default=0.25, env="QA_SECURITY_WEIGHT")
    QA_MAINTAINABILITY_WEIGHT: float = Field(default=0.15, env="QA_MAINTAINABILITY_WEIGHT")
    QA_DOCUMENTATION_WEIGHT: float = Field(default=0.15, env="QA_DOCUMENTATION_WEIGHT")
    
    # Quality Thresholds
    QA_MIN_SCORE: int = Field(default=60, env="QA_MIN_SCORE")
    QA_PASS_SCORE: int = Field(default=75, env="QA_PASS_SCORE")
    QA_EXCELLENT_SCORE: int = Field(default=90, env="QA_EXCELLENT_SCORE")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_REQUESTS_PER_MINUTE")
    RATE_LIMIT_BURST_SIZE: int = Field(default=10, env="RATE_LIMIT_BURST_SIZE")
    RATE_LIMIT_PATH_PREFIX: str = Field(default="/api/v1/", env="RATE_LIMIT_PATH_PREFIX")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173", "https://yourdomain.com"],
        env="CORS_ORIGINS"
    )
    CORS_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="CORS_METHODS"
    )
    CORS_HEADERS: List[str] = Field(default=["*"], env="CORS_HEADERS")
    CORS_CREDENTIALS: bool = Field(default=True, env="CORS_CREDENTIALS")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE_PATH: str = Field(default="./logs/app.log", env="LOG_FILE_PATH")
    LOG_ROTATION_SIZE: int = Field(default=10485760, env="LOG_ROTATION_SIZE")  # 10MB
    LOG_RETENTION_DAYS: int = Field(default=30, env="LOG_RETENTION_DAYS")
    LOG_MAX_FILES: int = Field(default=5, env="LOG_MAX_FILES")
    
    # Console Logging
    CONSOLE_LOG_LEVEL: str = Field(default="INFO", env="CONSOLE_LOG_LEVEL")
    CONSOLE_LOG_FORMAT: str = Field(default="colored", env="CONSOLE_LOG_FORMAT")
    
    # Performance Settings
    WORKER_PROCESSES: int = Field(default=4, env="WORKER_PROCESSES")
    WORKER_THREADS: int = Field(default=2, env="WORKER_THREADES")
    
    # Database Connection Pooling
    DB_POOL_SIZE: int = Field(default=10, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=20, env="DB_MAX_OVERFLOW")
    DB_POOL_TIMEOUT: int = Field(default=30, env="DB_POOL_TIMEOUT")
    
    # Cache Settings
    CACHE_DEFAULT_TTL: int = Field(default=300, env="CACHE_DEFAULT_TTL")
    CACHE_MAX_SIZE: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # Development Settings
    AUTO_RELOAD: bool = Field(default=True, env="AUTO_RELOAD")
    AUTO_RELOAD_DELAY: int = Field(default=1, env="AUTO_RELOAD_DELAY")
    DEBUG_SQL: bool = Field(default=False, env="DEBUG_SQL")
    DEBUG_WEBSOCKETS: bool = Field(default=False, env="DEBUG_WEBSOCKETS")
    DEBUG_MESSAGES: bool = Field(default=False, env="DEBUG_MESSAGES")
    
    # Test Database
    TEST_DATABASE_URL: str = Field(
        default="postgresql://emas_user:secure_password_123@localhost:5432/emas_test_db",
        env="TEST_DATABASE_URL"
    )
    
    # Kubernetes
    KUBERNETES_ENABLED: bool = Field(default=False, env="KUBERNETES_ENABLED")
    KUBERNETES_NAMESPACE: str = Field(default="emas", env="KUBERNETES_NAMESPACE")
    KUBERNETES_SERVICE_ACCOUNT: str = Field(default="emas-service-account", env="KUBERNETES_SERVICE_ACCOUNT")
    
    # Health Checks
    HEALTH_CHECK_ENABLED: bool = Field(default=True, env="HEALTH_CHECK_ENABLED")
    HEALTH_CHECK_PATH: str = Field(default="/health", env="HEALTH_CHECK_PATH")
    HEALTH_CHECK_INTERVAL: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    # Metrics
    METRICS_ENABLED: bool = Field(default=True, env="METRICS_ENABLED")
    METRICS_PATH: str = Field(default="/metrics", env="METRICS_PATH")
    METRICS_AUTH_REQUIRED: bool = Field(default=False, env="METRICS_AUTH_REQUIRED")
    
    # Feature Flags
    FEATURE_AI_ANALYSIS: bool = Field(default=True, env="FEATURE_AI_ANALYSIS")
    FEATURE_REAL_TIME_UPDATES: bool = Field(default=True, env="FEATURE_REAL_TIME_UPDATES")
    FEATURE_MULTI_TENANT: bool = Field(default=False, env="FEATURE_MULTI_TENANT")
    FEATURE_ADVANCED_METRICS: bool = Field(default=True, env="FEATURE_ADVANCED_METRICS")
    FEATURE_PERFORMANCE_MONITORING: bool = Field(default=True, env="FEATURE_PERFORMANCE_MONITORING")
    FEATURE_SECURITY_SCANNING: bool = Field(default=True, env="FEATURE_SECURITY_SCANNING")
    FEATURE_CODE_QUALITY: bool = Field(default=True, env="FEATURE_CODE_QUALITY")
    FEATURE_DOCUMENTATION_GENERATION: bool = Field(default=True, env="FEATURE_DOCUMENTATION_GENERATION")
    
    # Migration Settings
    AUTO_MIGRATE: bool = Field(default=False, env="AUTO_MIGRATE")
    MIGRATION_TIMEOUT: int = Field(default=60, env="MIGRATION_TIMEOUT")
    BACKUP_BEFORE_MIGRATION: bool = Field(default=True, env="BACKUP_BEFORE_MIGRATION")
    
    # Notification Settings
    SLACK_WEBHOOK_URL: Optional[str] = Field(default=None, env="SLACK_WEBHOOK_URL")
    SLACK_CHANNEL: str = Field(default="#emas-notifications", env="SLACK_CHANNEL")
    DISCORD_WEBHOOK_URL: Optional[str] = Field(default=None, env="DISCORD_WEBHOOK_URL")
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        allowed = ["development", "staging", "production", "test"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of: {allowed}")
        return v.upper()
    
    @validator("JWT_SECRET")
    def validate_jwt_secret(cls, v):
        if len(v) < 32:
            raise ValueError("JWT secret must be at least 32 characters long")
        return v
    
    @validator("PASSWORD_MIN_LENGTH")
    def validate_password_length(cls, v):
        if v < 8:
            raise ValueError("Password minimum length must be at least 8 characters")
        return v
    
    @validator("APP_PORT")
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "test"
    
    @property
    def supported_languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    def get_database_url(self) -> str:
        """Get database URL based on environment"""
        if self.is_testing:
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL
    
    def get_redis_url(self) -> str:
        """Get Redis URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    def get_smtp_config(self) -> dict:
        """Get SMTP configuration for email sending"""
        return {
            "host": self.SMTP_HOST,
            "port": self.SMTP_PORT,
            "username": self.SMTP_USER,
            "password": self.SMTP_PASSWORD,
            "use_tls": self.SMTP_USE_TLS,
            "use_ssl": self.SMTP_USE_SSL
        }
    
    def get_monitoring_config(self) -> dict:
        """Get monitoring configuration"""
        return {
            "prometheus": {
                "url": self.PROMETHEUS_URL,
                "enabled": self.PROMETHEUS_ENABLED
            },
            "grafana": {
                "url": self.GRAFANA_URL,
                "admin_user": self.GRAFANA_ADMIN_USER,
                "admin_password": self.GRAFANA_ADMIN_PASSWORD
            },
            "jaeger": {
                "url": self.JAEGER_URL,
                "enabled": self.JAEGER_ENABLED
            },
            "loki": {
                "url": self.LOKI_URL,
                "enabled": self.LOKI_ENABLED
            }
        }
    
    def get_agent_config(self) -> dict:
        """Get agent configuration"""
        return {
            "max_concurrent": self.AGENT_MAX_CONCURRENT,
            "timeout": self.AGENT_TIMEOUT,
            "retry_attempts": self.AGENT_RETRY_ATTEMPTS,
            "retry_delay": self.AGENT_RETRY_DELAY,
            "health_check_interval": self.AGENT_HEALTH_CHECK_INTERVAL,
            "types": {
                "code_analysis": self.CODE_ANALYSIS_AGENT_ENABLED,
                "test_generation": self.TEST_GENERATION_AGENT_ENABLED,
                "security_scanning": self.SECURITY_SCANNING_AGENT_ENABLED,
                "performance_analysis": self.PERFORMANCE_ANALYSIS_AGENT_ENABLED,
                "documentation": self.DOCUMENTATION_AGENT_ENABLED
            }
        }
    
    class Config:
        env_file = [".env", ".env.local"]
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()
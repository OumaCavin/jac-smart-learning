#!/bin/bash

# Start Backend Service Script
# FastAPI backend server startup script

set -e

echo "🚀 Starting JAC Smart Learning Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run 'bash setup.sh' first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export PYTHONPATH="${PWD}:${PYTHONPATH}"
export APP_ENV=development

# Check if .env file exists and load it
if [ -f ".env" ]; then
    echo "📄 Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

# Set default environment variables if not in .env
export APP_NAME="${APP_NAME:-JAC Smart Learning}"
export APP_VERSION="${APP_VERSION:-1.0.0}"
export APP_HOST="${APP_HOST:-0.0.0.0}"
export APP_PORT="${APP_PORT:-8000}"
export DEBUG="${DEBUG:-true}"
export LOG_LEVEL="${LOG_LEVEL:-info}"

# Database configuration
export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://cavin:Airtel!23!23@localhost:5432/jac_learning}"
export REDIS_URL="${REDIS_URL:-redis://localhost:6379/0}"
export NEO4J_URI="${NEO4J_URI:-bolt://localhost:7687}"
export NEO4J_USER="${NEO4J_USER:-neo4j}"
export NEO4J_PASSWORD="${NEO4J_PASSWORD:-password123}"

# API Keys
export OPENAI_API_KEY="${OPENAI_API_KEY:-your_openai_api_key_here}"
export SUPABASE_URL="${SUPABASE_URL:-your_supabase_url_here}"
export SUPABASE_ANON_KEY="${SUPABASE_ANON_KEY:-your_supabase_anon_key_here}"
export SUPABASE_SERVICE_ROLE_KEY="${SUPABASE_SERVICE_ROLE_KEY:-your_supabase_service_key_here}"

echo "🔧 Backend Configuration:"
echo "   - Host: $APP_HOST"
echo "   - Port: $APP_PORT"
echo "   - Debug: $DEBUG"
echo "   - Database: PostgreSQL"
echo "   - Cache: Redis"
echo "   - Graph DB: Neo4j"

# Check if Docker services are running
echo "🔍 Checking Docker services..."
if ! docker ps | grep -q jac-smart-learning_db_1; then
    echo "⚠️  Database services not running. Start them with: ./start_databases.sh"
fi

# Start FastAPI backend
echo "🖥️  Starting FastAPI server..."
echo "   Documentation: http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo ""

# Change to backend directory and start server
cd backend

# Use uvicorn to start the app with correct module path
uvicorn main:app \
    --host $APP_HOST \
    --port $APP_PORT \
    --reload \
    --log-level $LOG_LEVEL \
    --access-log

echo "✅ Backend stopped"
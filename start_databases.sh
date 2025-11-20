#!/bin/bash

# Start Database Services Script
# PostgreSQL, Redis, Neo4j, and NATS services via Docker Compose

set -e

echo "🐳 Starting Database Services with Docker Compose..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

# Use docker compose (v2) or docker-compose (v1) depending on availability
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Start services
echo "🔄 Starting database services..."
$COMPOSE_CMD up -d

echo ""
echo "⏳ Waiting for services to be ready..."

# Function to wait for service
wait_for_service() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    echo "🔍 Waiting for $service_name (port $port)..."
    
    while [ $attempt -le $max_attempts ]; do
        if timeout 1 bash -c "</dev/tcp/localhost/$port" >/dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "⚠️  $service_name took too long to start, but continuing..."
    return 1
}

# Wait for each service
wait_for_service "PostgreSQL" 5432
wait_for_service "Redis" 6379
wait_for_service "Neo4j" 7687
wait_for_service "NATS" 4222

echo ""
echo "🗄️  Database Services Status:"
$COMPOSE_CMD ps

echo ""
echo "📊 Service Information:"
echo "   PostgreSQL: localhost:5432 (jac_learning database)"
echo "   Redis:      localhost:6379"
echo "   Neo4j:      localhost:7474 (browser), localhost:7687 (bolt)"
echo "   NATS:       localhost:4222"
echo ""
echo "🔐 Default Credentials:"
echo "   PostgreSQL: cavin / Airtel!23!23"
echo "   Neo4j:      neo4j / password (change on first login)"
echo ""
echo "✅ Database services started successfully!"
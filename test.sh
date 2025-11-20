#!/bin/bash

# 🧪 JAC Smart Learning Test Script
# This script tests all components of your local installation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓ PASS]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗ FAIL]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Test database connections
test_databases() {
    print_status "Testing database connections..."
    
    # Test PostgreSQL
    if command -v psql &> /dev/null; then
        if psql -h localhost -U cavin -d jac_learning -c "SELECT version();" &> /dev/null; then
            print_success "PostgreSQL connection successful (DB: jac_learning)"
        else
            print_error "PostgreSQL connection failed"
        fi
    else
        print_warning "PostgreSQL client not installed, skipping PostgreSQL test"
    fi
    
    # Test Redis
    if command -v redis-cli &> /dev/null; then
        if redis-cli ping &> /dev/null; then
            print_success "Redis connection successful"
        else
            print_error "Redis connection failed"
        fi
    else
        print_warning "Redis client not installed, skipping Redis test"
    fi
    
    # Test Neo4j connection
    if curl -s http://localhost:7474 &> /dev/null; then
        print_success "Neo4j connection successful"
        print_status "Neo4j Browser available at http://localhost:7474 (login: neo4j/neo4j)"
    else
        print_error "Neo4j connection failed"
    fi
}

# Test backend API
test_backend_api() {
    print_status "Testing backend API..."
    
    # Test if API is running
    if curl -s http://localhost:8000/health &> /dev/null; then
        print_success "Backend API is running"
    else
        print_error "Backend API is not running on port 8000"
        print_warning "Make sure to run: ./start_backend.sh"
    fi
    
    # Test API documentation endpoint
    if curl -s http://localhost:8000/docs &> /dev/null; then
        print_success "API documentation is accessible"
    else
        print_error "API documentation is not accessible"
    fi
}

# Test frontend
test_frontend() {
    print_status "Testing frontend..."
    
    # Test if frontend is running
    if curl -s http://localhost:3000 &> /dev/null; then
        print_success "Frontend is running"
    else
        print_error "Frontend is not running on port 3000"
        print_warning "Make sure to run: ./start_frontend.sh"
    fi
}

# Test Python dependencies
test_dependencies() {
    print_status "Testing Python dependencies..."
    
    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate
        
        # Test key dependencies
        python -c "import fastapi" && print_success "FastAPI is installed"
        python -c "import uvicorn" && print_success "Uvicorn is installed"
        python -c "import sqlalchemy" && print_success "SQLAlchemy is installed"
        python -c "import redis" && print_success "Redis client is installed"
        python -c "import neo4j" && print_success "Neo4j driver is installed"
        
        # Test project imports
        python -c "import main" && print_success "Project modules can be imported"
        
    else
        print_error "Virtual environment not found"
    fi
}

# Test API endpoints
test_api_endpoints() {
    print_status "Testing API endpoints..."
    
    # Test CCG endpoint
    if curl -s -X POST "http://localhost:8000/api/v1/ccg/analyze" \
        -H "Content-Type: application/json" \
        -d '{"code": "print(\"Hello World\")", "language": "python"}' &> /dev/null; then
        print_success "CCG endpoint is working"
    else
        print_warning "CCG endpoint test failed (service might not be running)"
    fi
    
    # Test Quality Assessment endpoint
    if curl -s -X POST "http://localhost:8000/api/v1/quality/analyze/project" \
        -H "Content-Type: application/json" \
        -d '{"project_path": "/tmp"}' &> /dev/null; then
        print_success "Quality Assessment endpoint is working"
    else
        print_warning "Quality Assessment endpoint test failed (service might not be running)"
    fi
}

# Check Docker services
test_docker_services() {
    print_status "Testing Docker services..."
    
    if command -v docker &> /dev/null; then
        if docker ps | grep -q "postgres"; then
            print_success "PostgreSQL container is running"
        else
            print_warning "PostgreSQL container is not running"
        fi
        
        if docker ps | grep -q "redis"; then
            print_success "Redis container is running"
        else
            print_warning "Redis container is not running"
        fi
        
        if docker ps | grep -q "neo4j"; then
            print_success "Neo4j container is running"
        else
            print_warning "Neo4j container is not running"
        fi
    else
        print_warning "Docker is not available"
    fi
}

# Run all tests
run_all_tests() {
    echo "🧪 JAC Smart Learning System Test Suite"
    echo "=========================================="
    echo ""
    
    test_docker_services
    echo ""
    
    test_databases
    echo ""
    
    test_dependencies
    echo ""
    
    test_backend_api
    echo ""
    
    test_frontend
    echo ""
    
    test_api_endpoints
    echo ""
    
    echo "=========================================="
    echo "📋 Test Summary:"
    echo "Check the output above for any failed tests"
    echo "• Green [✓ PASS]: Component is working correctly"
    echo "• Red [✗ FAIL]: Component has issues"
    echo "• Yellow [WARNING]: Component may need attention"
    echo ""
    echo "🔧 If tests are failing:"
    echo "1. Make sure all services are started"
    echo "2. Check .env file configuration"
    echo "3. Verify database connections"
    echo "4. Run setup.sh if you haven't already"
    echo ""
}

# Main function
main() {
    run_all_tests
}

main "$@"
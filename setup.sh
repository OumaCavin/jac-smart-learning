#!/bin/bash

# 🛠️ Local Development Quick Setup Script
# Run this script to quickly set up your local development environment

set -e  # Exit on any error

echo "🚀 Starting JAC Smart Learning Local Setup..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    tools=("python" "git" "docker")
    for tool in "${tools[@]}"; do
        if ! command -v $tool &> /dev/null; then
            print_error "$tool is not installed. Please install it first."
            exit 1
        fi
    done
    
    # Check Python version
    python_version=$(python3 --version | cut -d' ' -f2)
    # Extract major and minor version numbers
    major_version=$(echo $python_version | cut -d'.' -f1)
    minor_version=$(echo $python_version | cut -d'.' -f2)
    
    # Check if Python 3.9+ (including 3.12)
    if [[ "$major_version" -lt 3 ]] || [[ "$major_version" -eq 3 && "$minor_version" -lt 9 ]]; then
        print_error "Python 3.9+ is required. Current version: $python_version"
        exit 1
    fi
    
    print_success "All prerequisites are installed!"
}

# Clone repository if not exists
setup_repository() {
    if [ ! -d ".git" ]; then
        print_status "Cloning repository..."
        git clone https://github.com/OumaCavin/jac-smart-learning.git .
        print_success "Repository cloned successfully!"
    else
        print_status "Repository already exists, pulling latest changes..."
        git pull origin main
    fi
}

# Setup Python backend
setup_backend() {
    print_status "Setting up Python backend..."
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created!"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    
    # Copy environment file if it doesn't exist
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_warning "Please edit .env file with your database credentials"
    fi
    
    print_success "Backend setup completed!"
}

# Setup database services
setup_databases() {
    print_status "Setting up database services..."
    
    # Check if docker-compose.yml exists
    if [ -f "docker-compose.yml" ]; then
        print_status "Starting databases with Docker..."
        docker-compose up -d
        
        print_status "Waiting for databases to be ready..."
        sleep 10
        
        # Check if containers are running
        if docker-compose ps | grep -q "Up"; then
            print_success "Databases started successfully!"
            print_status "Services available:"
            print_status "  - PostgreSQL: localhost:5432 (DB: jac_learning, User: cavin)"
            print_status "  - Redis: localhost:6379"
            print_status "  - Neo4j Browser: http://localhost:7474 (neo4j/neo4j)"
            print_status "  - Neo4j: bolt://localhost:7687"
        else
            print_error "Failed to start databases. Please check docker-compose logs."
            exit 1
        fi
    else
        print_warning "docker-compose.yml not found. Please set up databases manually."
    fi
}

# Setup Node.js frontend
setup_frontend() {
    print_status "Setting up Node.js frontend..."
    
    cd frontend
    
    # Check if Node.js is installed
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Install dependencies
    npm install
    
    cd ..
    
    print_success "Frontend setup completed!"
}

# Create startup scripts
create_scripts() {
    print_status "Creating startup scripts..."
    
    # Backend startup script
    cat > start_backend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Backend Server..."
source venv/bin/activate
echo "Activating virtual environment..."
echo "Starting FastAPI server on http://localhost:8000"
echo "API Documentation will be available at http://localhost:8000/docs"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOF

    # Frontend startup script
    cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Frontend Server..."
cd frontend
echo "Starting React development server on http://localhost:3000"
npm run dev
EOF

    # Database startup script
    cat > start_databases.sh << 'EOF'
#!/bin/bash
echo "🗄️  Starting Database Services..."
docker-compose up -d
echo "Databases started successfully!"
echo "Neo4j Browser: http://localhost:7474"
echo "PostgreSQL: localhost:5432"
echo "Redis: localhost:6379"
EOF

    # Make scripts executable
    chmod +x start_backend.sh start_frontend.sh start_databases.sh
    
    print_success "Startup scripts created!"
}

# Main setup function
main() {
    echo "Starting local setup process..."
    echo "This may take a few minutes..."
    
    check_prerequisites
    setup_repository
    setup_backend
    setup_databases
    setup_frontend
    create_scripts
    
    echo ""
    echo "=================================================="
    print_success "🎉 Setup completed successfully!"
    echo "=================================================="
    echo ""
    echo "📋 Next Steps:"
    echo "1. Edit .env file with your API keys (optional)"
    echo "2. Start databases: ./start_databases.sh"
    echo "3. Start backend:   ./start_backend.sh"
    echo "4. Start frontend:  ./start_frontend.sh"
    echo ""
    echo "🌐 Access Points:"
    echo "   Frontend:     http://localhost:3000"
    echo "   Backend API:  http://localhost:8000"
    echo "   API Docs:     http://localhost:8000/docs"
    echo "   Neo4j:        http://localhost:7474"
    echo ""
    echo "📚 For detailed instructions, see LOCAL_SETUP_GUIDE.md"
    echo ""
}

# Run main function
main "$@"
# 🛠️ Local Development Setup Guide

## Repository Access
**GitHub Repository:** https://github.com/OumaCavin/jac-smart-learning

## Prerequisites
- Python 3.9+ 
- Node.js 16+
- Docker & Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
# Clone the repository
git clone https://github.com/OumaCavin/jac-smart-learning.git
cd jac-smart-learning

# Verify the content
ls -la
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Database Setup

**Option A: Using Docker (Recommended)**
```bash
# Start all databases with Docker
docker-compose up -d

# Check if databases are running
docker ps
```

**Option B: Manual Database Setup**

*If you prefer to install databases manually:*

1. **PostgreSQL (v14+)**
   ```bash
   # Create database
   createdb jac_learning
   
   # Set environment variable
   export DATABASE_URL="postgresql://cavin:@localhost/jac_learning"
   ```

2. **Redis (v7+)**
   ```bash
   # Start Redis server
   redis-server
   ```

3. **Neo4j (v5+)**
   ```bash
   # Start Neo4j server
   neo4j start
   # Access at: http://localhost:7474
   # Default credentials: neo4j/neo4j
   ```

#### Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or your preferred editor
```

**Required Environment Variables:**
```bash
# Database Configuration
DATABASE_URL="postgresql://cavin:@localhost/jac_learning"
REDIS_URL="redis://localhost:6379"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="neo4j"

# API Keys (Optional for testing)
OPENAI_API_KEY="your_openai_key"
SUPABASE_URL="your_supabase_url"
SUPABASE_ANON_KEY="your_supabase_key"
GOOGLE_API_KEY="your_google_key"
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

### 4. Start the Application

**Terminal 1 - Backend:**
```bash
# From project root
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
# From frontend directory
cd frontend
npm run dev
```

### 5. Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Neo4j Browser:** http://localhost:7474

## 🔧 Testing the System

### Backend Testing
```bash
# Run all tests
pytest tests/ -v

# Test specific components
pytest tests/test_ccg_service.py -v
pytest tests/test_quality_assessment.py -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

### API Testing
```bash
# Test CCG service
curl -X POST "http://localhost:8000/api/v1/ccg/analyze" \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): return \"Hello World\"", "language": "python"}'

# Test Quality Assessment
curl -X POST "http://localhost:8000/api/v1/quality/analyze/project" \
  -H "Content-Type: application/json" \
  -d '{"project_path": "/path/to/your/code"}'
```

### Frontend Testing
Open http://localhost:3000 and test:
- User registration/login
- Code upload and analysis
- Quality assessment results
- Multi-agent system interaction

## 🐛 Troubleshooting

### Common Issues

**1. Database Connection Errors**
```bash
# Check database status
docker ps
# Restart databases
docker-compose restart
```

**2. Port Conflicts**
```bash
# Kill processes using ports
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:7474 | xargs kill -9  # Neo4j
```

**3. Dependency Issues**
```bash
# Clear and reinstall
pip cache purge
pip install -r requirements.txt --force-reinstall
npm install --force
```

**4. Neo4j Authentication**
```bash
# Reset Neo4j password
neo4j stop
neo4j-admin set-initial-password newpassword
neo4j start
```

### Development Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Hot reload
uvicorn main:app --reload

# Frontend with hot reload
npm run dev
```

## 📊 System Components

### Backend Services
- **FastAPI Server** (Port 8000)
- **CCGs Service** (Code Context Graph)
- **Quality Assessment** (5+ dimensions)
- **Multi-Agent System** (4 specialized agents)
- **WebSocket Support** (Real-time updates)

### Frontend Components
- **React Application** (Port 3000)
- **TypeScript + Tailwind CSS**
- **Code Editor** (Monaco Editor)
- **Real-time Updates** (WebSocket)

### Databases
- **PostgreSQL** (User data, sessions)
- **Redis** (Caching, real-time)
- **Neo4j** (Code relationships)

## 🚀 Next Steps

1. **Explore API Documentation:** http://localhost:8000/docs
2. **Test Multi-Agent System:** Upload code and see agents in action
3. **View Code Graphs:** Use Neo4j Browser to explore code relationships
4. **Run Quality Assessment:** Analyze project code quality
5. **Monitor System:** Check logs for real-time updates

## 📝 API Examples

### Code Analysis
```python
import requests

# Analyze Python code
response = requests.post('http://localhost:8000/api/v1/ccg/analyze', json={
    'code': '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''',
    'language': 'python'
})
print(response.json())
```

### Quality Assessment
```python
# Assess project quality
response = requests.post('http://localhost:8000/api/v1/quality/analyze/project', json={
    'project_path': '/path/to/your/python/project'
})
print(response.json())
```

## 🔒 Security Notes

- **Never commit real API keys** to version control
- **Use environment variables** for sensitive data
- **Enable HTTPS** in production
- **Configure CORS** properly for your domain

---

## Support

If you encounter issues:
1. Check the logs in the terminal
2. Verify all services are running with `docker ps`
3. Test database connectivity
4. Check the API documentation at `/docs`

Happy coding! 🎉
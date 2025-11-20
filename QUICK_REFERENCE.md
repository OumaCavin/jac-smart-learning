# 🚀 JAC Smart Learning - Quick Reference Card

## 📦 Repository
**GitHub**: https://github.com/OumaCavin/jac-smart-learning

## ⚡ One-Command Setup
```bash
git clone https://github.com/OumaCavin/jac-smart-learning.git && cd jac-smart-learning && bash setup.sh
```

## 🎯 Essential Commands

### Setup & Installation
```bash
# Clone & Setup
git clone https://github.com/OumaCavin/jac-smart-learning.git
cd jac-smart-learning
bash setup.sh

# Manual Setup
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd frontend && npm install
docker-compose up -d
```

### Starting Services
```bash
# Start Databases
./start_databases.sh
# OR: docker-compose up -d

# Start Backend
./start_backend.sh
# OR: uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start Frontend  
./start_frontend.sh
# OR: cd frontend && npm run dev
```

### Testing
```bash
# Run all tests
bash test.sh

# Backend tests
pytest tests/ -v

# API testing
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

## 🌐 Access Points
| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend Dashboard** | http://localhost:3000 | Main UI |
| **Backend API** | http://localhost:8000 | API Server |
| **API Docs** | http://localhost:8000/docs | Interactive API Docs |
| **Neo4j Browser** | http://localhost:7474 | Graph Database |
| **PostgreSQL** | localhost:5432 | Main Database |
| **Redis** | localhost:6379 | Cache/Sessions |

## 🔧 Environment Configuration

### Required Environment Variables
```bash
# .env file
DATABASE_URL="postgresql://cavin:@localhost/jac_learning"
REDIS_URL="redis://localhost:6379"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="neo4j"

# Optional API Keys
OPENAI_API_KEY="your_key_here"
SUPABASE_URL="your_supabase_url"
GOOGLE_API_KEY="your_google_key"
```

## 📚 Documentation Files
- **LOCAL_SETUP_GUIDE.md** - Complete setup instructions
- **README.md** - Main project documentation
- **JAC_Complete_Learning_Guide.md** - JAC language learning
- **api/openapi/openapi.yaml** - API reference

## 🐛 Troubleshooting

### Common Issues & Solutions

**1. Port Already in Use**
```bash
# Kill processes using ports
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:7474 | xargs kill -9  # Neo4j
```

**2. Database Connection Issues**
```bash
# Restart databases
docker-compose restart
# Check status
docker-compose ps
```

**3. Virtual Environment Issues**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Neo4j Authentication**
```bash
# Reset Neo4j password
neo4j stop
neo4j-admin set-initial-password newpassword
neo4j start
```

## 🧪 API Testing Examples

### Code Context Graph (CCG)
```bash
# Analyze code
curl -X POST "http://localhost:8000/api/v1/ccg/analyze" \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): return \"Hello World\"", "language": "python"}'

# Get dependencies
curl "http://localhost:8000/api/v1/ccg/dependencies?file_path=main.py"
```

### Quality Assessment
```bash
# Assess project
curl -X POST "http://localhost:8000/api/v1/quality/analyze/project" \
  -H "Content-Type: application/json" \
  -d '{"project_path": "/path/to/your/code"}'

# Assess file
curl -X POST "http://localhost:8000/api/v1/quality/analyze/file" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "main.py", "source_directory": "/path/to/project"}'
```

### Multi-Agent System
```bash
# Get agent status
curl http://localhost:8000/api/v1/agents/status

# Start agent task
curl -X POST "http://localhost:8000/api/v1/agents/tasks" \
  -H "Content-Type: application/json" \
  -d '{"task_type": "code_analysis", "payload": {"code": "..."}}'
```

## 📊 System Status Check
```bash
# Run comprehensive test
bash test.sh

# Check individual services
curl http://localhost:8000/health
curl http://localhost:3000
curl http://localhost:7474

# Check Docker containers
docker-compose ps
docker logs postgres
docker logs redis
docker logs neo4j
```

## 🔧 Development Workflow

### Backend Development
```bash
# Activate environment
source venv/bin/activate

# Run with hot reload
uvicorn main:app --reload

# Run tests
pytest tests/ -v

# Code formatting
black .
flake8 .
mypy .
```

### Frontend Development
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Database Management
```bash
# Connect to PostgreSQL
psql -h localhost -U cavin -d jac_learning

# Connect to Redis
redis-cli

# Access Neo4j
open http://localhost:7474
# Default login: neo4j/neo4j
```

## 🚀 Production Deployment

### Docker Production
```bash
# Build and run
docker build -t jac-smart-learning .
docker run -p 8000:8000 jac-smart-learning
```

### Kubernetes Deployment
```bash
# Deploy to K8s
kubectl apply -f k8s/

# Check deployment
kubectl get pods
kubectl logs -f deployment/backend
```

## 📞 Support & Help

### Documentation
- **Main README**: See README.md for complete documentation
- **Setup Guide**: See LOCAL_SETUP_GUIDE.md for detailed instructions
- **API Reference**: http://localhost:8000/docs (when server is running)

### Contact Information
- **Email**: cavin.otieno012@gmail.com
- **WhatsApp**: +254708101604
- **LinkedIn**: https://www.linkedin.com/in/cavin-otieno-9a841260/

### Getting Help
1. Check the troubleshooting section above
2. Run `bash test.sh` to identify issues
3. Check logs in terminal for error messages
4. Consult API documentation at /docs endpoint
5. Contact support using the information above

---

## 🎉 Success Indicators

Your installation is working correctly when:
- ✅ Frontend loads at http://localhost:3000
- ✅ Backend API responds at http://localhost:8000
- ✅ API documentation accessible at http://localhost:8000/docs
- ✅ All Docker containers running (`docker-compose ps`)
- ✅ Test suite passes (`bash test.sh`)

**Happy Coding! 🚀**
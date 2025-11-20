# 🚀 Enterprise Multi-Agent System (EMAS)

> **Author**: Cavin Otieno  
> **Contact**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com) | [LinkedIn](https://www.linkedin.com/in/cavin-otieno-9a841260/) | **WhatsApp**: [+254708101604](https://wa.me/254708101604)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](CHANGELOG.md)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/OumaCavin/jac-smart-learning/actions)
[![Documentation](https://img.shields.io/badge/Docs-Complete-blue.svg)](docs/)
[![Coverage](https://img.shields.io/badge/Coverage-85%25-brightgreen.svg)](coverage/)

---

## 🎯 Overview

Enterprise Multi-Agent System (EMAS) is a production-ready, scalable, and feature-rich platform that orchestrates multiple intelligent agents to solve complex problems. Built with JAC programming language integration and featuring cutting-edge technologies like Object-Spatial Programming (OSP) and AI-powered code analysis.

### ✨ Key Features

- **🤖 Multi-Agent Orchestration**: Advanced coordination system with Chain of Responsibility pattern
- **⚡ Real-Time Updates**: WebSocket-based live progress tracking and monitoring
- **🧠 Code Context Graph (CCG)**: Deep code understanding through AST analysis and graph relationships
  - **AST Parsing**: Comprehensive parsing of Python source code
  - **Graph Relationships**: Call graphs, inheritance hierarchies, and dependency mapping
  - **Neo4j Storage**: Graph database for advanced query capabilities
  - **Real-time Analysis**: Live codebase analysis and visualization
- **🎯 Quality Assessment Engine**: Multi-dimensional code evaluation (5+ dimensions)
  - **Correctness**: Syntax validation, type hints coverage, logical structure analysis
  - **Performance**: Cyclomatic complexity, algorithm efficiency, nested loop detection
  - **Security**: Vulnerability scanning, pattern detection, code injection prevention
  - **Code Quality**: Style compliance, naming conventions, maintainability metrics
  - **Documentation**: Docstring coverage, documentation quality, API completeness
- **📊 Scalable Architecture**: Microservices design with Kubernetes autoscaling
- **🔒 Enterprise Security**: Comprehensive auth, secrets management, and compliance
- **📈 Monitoring & Observability**: Complete observability stack with Prometheus, Grafana, and Jaeger
- **🚀 CI/CD Ready**: Automated testing, deployment, and secret scanning
- **🧪 Comprehensive Testing**: Unit, integration, and end-to-end test suites
- **📚 JAC Integration**: Built-in support for Jaseci programming language features

---

## 🏗️ Architecture Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        React[React Dashboard]
        WebSocket[WebSocket Client]
    end
    
    subgraph "API Gateway"
        Gateway[API Gateway]
        LoadBalancer[Load Balancer]
    end
    
    subgraph "Core Services"
        Orchestrator[Agent Orchestrator]
        MessageBus[Message Bus]
        CCGService[Code Context Graph]
        QAService[Quality Assessment]
    end
    
    subgraph "Agent Types"
        CodeAgent[Code Analysis Agent]
        TestAgent[Test Generation Agent]
        SecurityAgent[Security Agent]
        PerfAgent[Performance Agent]
        DocAgent[Documentation Agent]
    end
    
    subgraph "Data Layer"
        GraphDB[(Graph Database)]
        Redis[(Redis Cache)]
        Postgres[(PostgreSQL)]
    end
    
    subgraph "Infrastructure"
        K8s[Kubernetes Cluster]
        Monitor[Monitoring Stack]
        Log[Centralized Logging]
    end
    
    React --> Gateway
    WebSocket --> Gateway
    Gateway --> Orchestrator
    Orchestrator --> MessageBus
    MessageBus --> CodeAgent
    MessageBus --> TestAgent
    MessageBus --> SecurityAgent
    MessageBus --> PerfAgent
    MessageBus --> DocAgent
    CCGService --> GraphDB
    QAService --> Redis
    Orchestrator --> Postgres
    K8s --> Monitor
    K8s --> Log
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** (v20.10+) and **Docker Compose**
- **Kubernetes** (v1.20+) for production deployments
- **Node.js** (v18+) for frontend development
- **Python** (v3.9+) for backend services
- **Git** configured with username `OumaCavin`

### Installation

```bash
# Clone the repository
git clone https://github.com/OumaCavin/jac-smart-learning.git
cd jac-smart-learning

# Setup environment
cp .env.example .env
cp .env.local.example .env.local

# Start with Docker Compose (recommended for development)
docker-compose up -d

# Or deploy to Kubernetes
kubectl apply -f k8s/
```

### Environment Variables

Create `.env` file with the following configuration:

```bash
# Database Configuration
DATABASE_URL=postgresql://emas_user:secure_password@localhost:5432/emas_db
REDIS_URL=redis://localhost:6379/0

# Authentication
JWT_SECRET=<JWT_SECRET_PLACEHOLDER>
GITHUB_CLIENT_ID=<GITHUB_CLIENT_ID_PLACEHOLDER>
GITHUB_CLIENT_SECRET=<GITHUB_CLIENT_SECRET_PLACEHOLDER>

# AI/LLM Integration
OPENAI_API_KEY=<OPENAI_API_KEY_PLACEHOLDER>
SUPABASE_URL=https://rjgrobamzmbcvakwltxt.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqZ3JvYmFtem1iY3Zha3dsdHh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1ODc2ODQsImV4cCI6MjA3OTE2MzY4NH0.NH6i7UUor07PevpK7AMzMw7LvLP8j9wtuypfa_azip0
SUPABASE_SERVICE_ROLE=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqZ3JvYmFtem1iY3Zha3dsdHh0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzU4NzY4NCwiZXhwIjoyMDc5MTYzNjg0fQ.5m60ck3umars1l2_Yz-BOI5URajEZoDqELkcVglv2lA
SUPABASE_DB_PASSWORD=Airtel!23!23

# Monitoring
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000
JAEGER_URL=http://jaeger:16686

# Message Bus
NATS_URL=nats://nats:4222
NATS_USER=<NATS_USER_PLACEHOLDER>
NATS_PASSWORD=<NATS_PASSWORD_PLACEHOLDER>

# Security
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=<VAULT_TOKEN_PLACEHOLDER>

# Email Configuration
GMAIL_USER=cavin.otieno012@gmail.com
GMAIL_APP_PASSWORD=<GMAIL_APP_PASSWORD_PLACEHOLDER>
```

---

## 📖 Documentation

### 📚 Core Documentation

- **[Architecture Guide](docs/architecture/README.md)** - System design and architecture patterns
- **[API Reference](api/openapi/openapi.yaml)** - Complete API documentation
- **[Deployment Guide](docs/deployment/README.md)** - Production deployment instructions
- **[User Guide](docs/user-guide/README.md)** - End-user documentation
- **[Contributing Guide](CONTRIBUTING.md)** - Development and contribution guidelines

### 🛠️ Development Guides

- **[Quick Reference](JAC_Quick_Reference.md)** - JAC language quick reference
- **[Learning Guide](JAC_Complete_Learning_Guide.md)** - Complete JAC learning resource
- **[Examples](examples/)** - Practical code examples and tutorials

---

## 🧪 Testing & Quality

### Running Tests

```bash
# Run all tests
make test

# Run unit tests
make test-unit

# Run integration tests
make test-integration

# Run end-to-end tests
make test-e2e

# Run load tests
make test-load

# Run security tests
make test-security

# Generate coverage report
make coverage
```

### Quality Metrics

- **Test Coverage**: 85%+ target
- **Security Scan**: Passed
- **Performance**: < 200ms API response time
- **Availability**: 99.9% uptime SLA

---

## 🔌 API Reference

### Code Context Graph (CCG) API

```bash
# Analyze entire codebase
POST /api/v1/ccg/analyze
{
  "source_directory": "/path/to/source",
  "file_patterns": ["*.py"]
}

# Get file dependencies
GET /api/v1/ccg/dependencies?file_path=src/main.py

# Get call graph for function
GET /api/v1/ccg/call-graph?function_name=process_data

# Get class hierarchy
GET /api/v1/ccg/class-hierarchy

# Get CCG metrics
GET /api/v1/ccg/metrics
```

### Quality Assessment API

```bash
# Assess single file
POST /api/v1/quality/assess/file
{
  "file_path": "src/main.py",
  "source_directory": "/path/to/project"
}

# Assess entire project
POST /api/v1/quality/assess/project
{
  "project_path": "/path/to/project"
}

# Assess specific dimension
POST /api/v1/quality/assess/dimension
{
  "dimension": "security",
  "file_path": "src/main.py",
  "source_directory": "/path/to/project"
}

# Validate code in real-time
POST /api/v1/quality/validate/code
{
  "code_content": "def hello(): pass",
  "filename": "test.py"
}

# Get available dimensions
GET /api/v1/quality/dimensions
```

### Response Examples

**CCG Analysis Response:**
```json
{
  "success": true,
  "files_processed": ["main.py", "utils.py", "models.py"],
  "nodes_count": 45,
  "edges_count": 78,
  "metrics": {
    "total_nodes": 45,
    "total_edges": 78,
    "node_types": {
      "function": 12,
      "class": 3,
      "method": 15
    }
  }
}
```

**Quality Assessment Response:**
```json
{
  "success": true,
  "file_path": "main.py",
  "overall_score": 0.85,
  "scores": {
    "correctness": {
      "dimension": "correctness",
      "score": 0.9,
      "level": "EXCELLENT",
      "suggestions": ["Add type hints"]
    },
    "security": {
      "dimension": "security", 
      "score": 0.8,
      "level": "GOOD",
      "violations": []
    }
  }
}
```

**API Documentation**
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: `/openapi.json`

---

## 🚢 Deployment Options

### Development (Docker Compose)

```bash
# Quick start
docker-compose up -d

# With monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

### Production (Kubernetes)

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Using Helm
helm install emas ./k8s/helm/emas
```

### Platform as a Service

```bash
# Deploy to Vercel (Frontend)
vercel --prod

# Deploy to Heroku (Backend)
heroku create jac-smart-learning-api
git push heroku main
```

---

## 📊 Monitoring & Observability

### Metrics Dashboard

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Jaeger Tracing**: http://localhost:16686
- **Loki Logs**: http://localhost:3100

### Key Metrics

- **Agent Performance**: Response times, success rates
- **System Health**: CPU, memory, disk usage
- **Business Metrics**: Tasks completed, user activity
- **Quality Metrics**: Code quality scores, security findings

---

## 🔧 Configuration

### Agent Configuration

Agents are configured through YAML files in `src/agents/config/`:

```yaml
# Example agent configuration
code_analysis_agent:
  name: "Code Analysis Agent"
  version: "1.0.0"
  max_concurrent_tasks: 10
  timeout: 300
  retry_policy:
    max_retries: 3
    backoff_strategy: "exponential"
```

### Scaling Configuration

```yaml
# HPA Configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: emas-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: emas-backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 🛡️ Security

### Security Features

- **Authentication**: JWT-based with OAuth2
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: End-to-end encryption for sensitive data
- **Secret Management**: HashiCorp Vault integration
- **Security Scanning**: Automated dependency scanning
- **Compliance**: SOC2 and GDPR ready

### Security Best Practices

```bash
# Run security scan
make security-scan

# Audit dependencies
npm audit
pip-audit

# Secret scanning
trufflehog .
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and setup
git clone https://github.com/OumaCavin/jac-smart-learning.git
cd jac-smart-learning

# Install dependencies
npm install
pip install -r requirements.txt

# Start development
make dev

# Run tests
make test
```

### Commit Guidelines

- Use meaningful commit messages
- Follow conventional commits format
- Example: `feat(ccg): add AST parser and initial graph export — written by developer (OumaCavin)`

---

## 📞 Support

### Get Help

- **📧 Email**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com)
- **💬 WhatsApp**: [+254708101604](https://wa.me/254708101604)
- **💼 LinkedIn**: [Cavin Otieno](https://www.linkedin.com/in/cavin-otieno-9a841260/)
- **📖 Documentation**: [docs/](docs/)
- **🐛 Issues**: [GitHub Issues](https://github.com/OumaCavin/jac-smart-learning/issues)

### Office Hours

Join our weekly office hours for mentorship and technical discussions:
- **Schedule**: Every Tuesday 2:00 PM EAT
- **Format**: Google Meet (link shared in GitHub discussions)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Jaseci Team** for the amazing JAC programming language
- **OpenAI** for GPT-powered code analysis features
- **Supabase** for the robust backend infrastructure
- **Kubernetes Community** for scalable deployment solutions

---

**Built with ❤️ by Cavin Otieno**

> *"Transforming code into intelligent, self-improving systems through advanced multi-agent orchestration."*
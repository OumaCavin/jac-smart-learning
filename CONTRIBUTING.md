# Contributing Guide

**Author**: Cavin Otieno  
**Contact**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com) | **WhatsApp**: [+254708101604](https://wa.me/254708101604)

Thank you for your interest in contributing to the Enterprise Multi-Agent System (EMAS)! This guide will help you get started with development and understand our contribution process.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Git** (configured with username `OumaCavin`)
- **Docker** (v20.10+) and **Docker Compose**
- **Node.js** (v18+) and **npm** or **pnpm**
- **Python** (v3.9+)
- **Kubernetes** (for production deployments)
- **GitHub CLI** (optional but recommended)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/OumaCavin/jac-smart-learning.git
cd jac-smart-learning

# Setup Git configuration
git config user.name "OumaCavin"
git config user.email "cavin.otieno012@gmail.com"

# Setup development environment
make setup-dev

# Start development services
make dev
```

### Repository Structure

```
jac-smart-learning/
├── 📁 src/                   # Core source code
│   ├── orchestrator/         # Multi-agent orchestration
│   ├── agents/              # Agent implementations
│   ├── messaging/           # Message bus and communication
│   ├── ccg/                 # Code Context Graph services
│   ├── qa-engine/           # Quality assessment engine
│   ├── auth/                # Authentication & authorization
│   └── database/            # Database models and migrations
├── 📁 backend/              # Backend services
│   ├── api/                 # REST API endpoints
│   ├── websocket/           # WebSocket handlers
│   ├── core/                # Core business logic
│   └── services/            # Microservices
├── 📁 frontend/             # React dashboard
│   ├── src/components/      # Reusable components
│   ├── src/pages/           # Page components
│   ├── src/store/           # State management
│   └── public/              # Static assets
├── 📁 docs/                 # Documentation
│   ├── architecture/        # Architecture documentation
│   ├── api/                 # API specifications
│   ├── deployment/          # Deployment guides
│   └── user-guide/          # User documentation
├── 📁 infra/                # Infrastructure
│   ├── docker/              # Docker configurations
│   ├── compose/             # Docker Compose files
│   └── helm/                # Helm charts
├── 📁 k8s/                  # Kubernetes manifests
├── 📁 tests/                # Test suites
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   ├── e2e/                 # End-to-end tests
│   ├── load/                # Load tests
│   └── security/            # Security tests
├── 📁 monitoring/           # Observability stack
└── 📁 security/             # Security configurations
```

## 🛠️ Development Workflow

### Branch Strategy

We follow a simple but effective branching strategy:

- **main**: Production-ready code
- **feature/description**: New features or enhancements
- **bugfix/description**: Bug fixes
- **hotfix/description**: Critical production fixes

### Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```bash
# Feature development
feat(ccg): add AST parser and initial graph export — written by developer (OumaCavin)
feat(api): implement WebSocket endpoint for real-time updates

# Bug fixes
fix(orchestrator): resolve memory leak in agent pool manager

# Documentation
docs(api): add endpoint documentation for quality assessment

# Refactoring
refactor(messaging): optimize message routing algorithm

# Testing
test(ccg): add unit tests for graph generation pipeline
```

### Development Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement Changes**
   - Follow our [Code Standards](#code-standards)
   - Write comprehensive tests
   - Update documentation

3. **Test Your Changes**
   ```bash
   make test           # Run all tests
   make lint           # Check code quality
   make security-scan  # Security audit
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat(ccg): add AST parser and initial graph export — written by developer (OumaCavin)"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Fill out the PR template
   - Link related issues
   - Request reviews from maintainers

## 📝 Code Standards

### Code Style

#### Python (Backend)
- Follow [PEP 8](https://pep8.org/) style guide
- Use **Black** for code formatting
- Use **isort** for import sorting
- Follow **type hints** for all functions
- Document functions with **docstrings**

```python
def analyze_code_quality(code: str, language: str) -> QualityReport:
    """
    Analyze code quality using multiple metrics.
    
    Args:
        code: Source code to analyze
        language: Programming language of the code
        
    Returns:
        QualityReport containing analysis results
        
    Raises:
        ValueError: If language is not supported
    """
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")
    
    # Implementation here...
    return QualityReport(...)
```

#### JavaScript/TypeScript (Frontend)
- Use **ESLint** and **Prettier** configurations
- Follow **TypeScript strict mode** guidelines
- Use **React Hooks** for state management
- Implement **proper error boundaries**

```typescript
interface AgentMetrics {
  id: string;
  name: string;
  status: 'active' | 'idle' | 'error';
  performance: PerformanceMetrics;
}

const useAgentMetrics = (agentId: string): UseAgentMetricsResult => {
  const [metrics, setMetrics] = useState<AgentMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Implementation here...
  }, [agentId]);

  return { metrics, loading, error };
};
```

#### JAC Programming
- Use strong typing with explicit type declarations
- Leverage **Object-Spatial Programming** for graph operations
- Implement **walkers** for efficient graph traversal
- Use **byLLM** for AI integration

```jac
# Define node archetype
node CodeFile {
    has name: str;
    has content: str;
    has language: str;
    has quality_score: float = 0.0;
}

# Define walker for code analysis
walker analyze_code_quality {
    has target_file: str;
    has language: str;
    
    can parse_ast, calculate_metrics, generate_report;
    
    with entry {
        report("Starting code quality analysis");
    }
    
    with exit {
        report("Analysis completed successfully");
    }
}
```

### Testing Standards

#### Unit Tests
- **Coverage**: Minimum 80% for all new code
- **Frameworks**: 
  - Python: `pytest` with `pytest-asyncio`
  - JavaScript: `Jest` with `Testing Library`
- **Naming**: Test files should be `test_*.py` or `*.test.js`

```python
def test_ccg_ast_parser_valid_code():
    """Test AST parsing with valid JavaScript code."""
    code = "function hello(name) { return 'Hello ' + name; }"
    parser = CCGASTParser()
    ast = parser.parse(code, "javascript")
    
    assert ast is not None
    assert ast["type"] == "Program"
    assert len(ast["body"]) == 1

@pytest.mark.asyncio
async def test_websocket_agent_updates():
    """Test WebSocket connection for real-time agent updates."""
    client = TestWebSocketClient()
    await client.connect("ws://localhost:8080/ws")
    
    # Test message handling
    await client.send({"type": "subscribe", "agent_id": "test-agent"})
    response = await client.receive()
    
    assert response["type"] == "subscription_confirmed"
    await client.close()
```

#### Integration Tests
- Test API endpoints with real database connections
- Use **test containers** for database testing
- Mock external services with **pytest-mock** or **sinon**

#### End-to-End Tests
- Use **Playwright** for browser automation
- Test complete user workflows
- Include performance assertions

### Documentation Standards

#### API Documentation
- Use **OpenAPI 3.0** specification
- Include request/response examples
- Document all error codes and edge cases

```yaml
# Example OpenAPI specification
paths:
  /api/v1/agents/analyze:
    post:
      summary: Analyze code with multiple agents
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnalysisRequest'
      responses:
        '200':
          description: Analysis completed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AnalysisResponse'
        '400':
          description: Invalid request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
```

#### Code Documentation
- Document all public APIs and interfaces
- Include usage examples
- Maintain **docstrings** for all functions and classes
- Add **README** sections for new features

## 🧪 Testing Guidelines

### Test Types

1. **Unit Tests**: Individual function/component testing
2. **Integration Tests**: Service-to-service interaction testing
3. **End-to-End Tests**: Complete workflow testing
4. **Load Tests**: Performance and scalability testing
5. **Security Tests**: Vulnerability and penetration testing

### Running Tests

```bash
# All tests
make test

# Specific test types
make test-unit
make test-integration
make test-e2e
make test-load
make test-security

# With coverage
make coverage

# Watch mode
make test-watch
```

### Test Data

- Use **factories** for test data generation
- Implement **fixtures** for common test scenarios
- Clean up test data after each test run

## 🔧 Development Tools

### Recommended VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "redhat.vscode-yaml",
    "ms-vscode-remote.remote-containers"
  ]
}
```

### Git Hooks

We use **pre-commit** hooks for code quality:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## 🚀 Deployment Process

### Staging Environment

1. **Feature Testing**: All features tested in staging
2. **Performance Testing**: Load testing before production
3. **Security Scanning**: Vulnerability assessment
4. **User Acceptance**: Stakeholder approval required

### Production Deployment

1. **CI/CD Pipeline**: Automated testing and deployment
2. **Blue-Green Deployment**: Zero-downtime deployments
3. **Monitoring**: Real-time health checks and alerts
4. **Rollback Plan**: Quick rollback capability

## 🔒 Security Guidelines

### Secret Management

- **Never** commit secrets to the repository
- Use **environment variables** for sensitive data
- Implement **secret rotation** policies
- Use **HashiCorp Vault** or **AWS Secrets Manager**

### Security Best Practices

- **Input Validation**: Validate all user inputs
- **SQL Injection**: Use parameterized queries
- **XSS Prevention**: Sanitize user-generated content
- **Authentication**: Implement proper session management
- **Authorization**: Use role-based access control

### Reporting Security Issues

If you discover a security vulnerability, please email **Cavin Otieno** at [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com) with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fixes (if any)

## 🎯 Areas for Contribution

### High Priority
- **Code Context Graph (CCG)** improvements
- **Quality Assessment Engine** enhancements
- **Real-time WebSocket** optimizations
- **Security scanning** integrations
- **Performance optimizations**

### Medium Priority
- **Documentation** improvements
- **UI/UX** enhancements
- **Test coverage** expansion
- **Monitoring** dashboard improvements
- **Deployment** automation

### Low Priority
- **Feature requests** from community
- **Code refactoring** for maintainability
- **Dependency** updates
- **Accessibility** improvements

## 📞 Getting Help

### Communication Channels

- **Email**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com)
- **WhatsApp**: [+254708101604](https://wa.me/254708101604)
- **GitHub Discussions**: Community Q&A
- **Issues**: Bug reports and feature requests

### Office Hours

Join our weekly **office hours** for mentorship and technical discussions:
- **Schedule**: Every Tuesday 2:00 PM EAT
- **Format**: Google Meet (link shared in GitHub discussions)

### Mentoring Program

We offer structured mentorship for contributors:
- **Beginner**: Introduction to the codebase and development process
- **Intermediate**: Feature development and advanced concepts
- **Advanced**: Architecture decisions and project leadership

## 🎉 Recognition

### Contributor Levels

1. **Bronze**: First contribution
2. **Silver**: Multiple quality contributions
3. **Gold**: Significant feature implementations
4. **Platinum**: Core maintainer status

### Hall of Fame

Contributors who make exceptional contributions will be featured in:
- Project documentation
- Release notes
- Conference presentations
- Technical blog posts

---

## 🙏 Thank You!

Thank you for contributing to the Enterprise Multi-Agent System! Your involvement helps make this project better for everyone. We appreciate your time and effort in making this a robust, scalable, and user-friendly platform.

**Remember**: Every contribution, no matter how small, makes a difference. Start with the areas that interest you most, and don't hesitate to ask questions!

---

**Built with ❤️ by Cavin Otieno**

*Questions? Reach out at [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com) or [+254708101604](https://wa.me/254708101604)*
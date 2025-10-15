# Contributing Guide

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 🤝 How to Contribute

We welcome contributions to the AI Agent Starter Pack! This guide will help you get started with contributing to the project.

## 🚀 Getting Started

### **Fork and Clone**
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/your-username/ai-agent-starter-pack.git
cd ai-agent-starter-pack

# Add upstream remote
git remote add upstream https://github.com/original-repo/ai-agent-starter-pack.git
```

### **Development Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration
```

### **Run Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_health_service.py -v

# Run with coverage
python -m pytest tests/ --cov=.
```

## 📝 Contribution Types

### **Bug Reports**
When reporting bugs, please include:
- **Description**: Clear description of the bug
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, dependencies
- **Screenshots**: If applicable

### **Feature Requests**
When requesting features, please include:
- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Additional Context**: Any other relevant information

### **Code Contributions**
When contributing code:
- **Follow Architecture**: Maintain Clean Architecture principles
- **Write Tests**: Include unit and integration tests
- **Update Documentation**: Update relevant documentation
- **Follow Style**: Follow existing code style and patterns

## 🏗️ Architecture Guidelines

### **Clean Architecture**
Follow the established Clean Architecture pattern:

```
domain/          # Core business logic
application/      # Use cases and orchestration
infrastructure/  # External dependencies
presentation/    # APIs and user interfaces
```

### **Dependency Injection**
Use the DI container for service registration:

```python
# Register new service
class Container:
    new_service = providers.Singleton(NewService)
```

### **Railway Oriented Programming**
Use the Result pattern for error handling:

```python
# Success case
result = await service.operation()
if result.is_success:
    data = result.value
else:
    error = result.error
```

### **Microservices Pattern**
Break down complex services into smaller, focused services:

```python
# Main service (Facade)
class MainService:
    def __init__(self, sub_service1, sub_service2):
        self.sub_service1 = sub_service1
        self.sub_service2 = sub_service2

# Sub-services
class SubService1:
    pass

class SubService2:
    pass
```

## 🧪 Testing Guidelines

### **Test Structure**
```python
# Test file naming
test_service_name.py

# Test class naming
class TestServiceName:
    pass

# Test method naming
def test_method_name():
    pass
```

### **Test Categories**
- **Unit Tests**: Test individual components
- **Integration Tests**: Test service interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test system performance

### **Test Examples**
```python
import pytest
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService

@pytest.mark.asyncio
async def test_lmstudio_embedding():
    """Test LM Studio embedding service."""
    service = LMStudioEmbeddingService(
        proxy_url="http://127.0.0.1:8123",
        model_name="model:10"
    )
    
    result = await service.create_embedding("test")
    assert result.is_success
    assert len(result.value) > 0
    assert isinstance(result.value[0], float)
```

## 📚 Documentation Guidelines

### **Code Documentation**
```python
class ServiceName:
    """
    Service description.
    
    This service provides functionality for...
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Example:
        service = ServiceName(param1="value1", param2="value2")
        result = await service.operation()
    """
    
    async def method_name(self, param: str) -> Result[str, str]:
        """
        Method description.
        
        Args:
            param: Parameter description
            
        Returns:
            Result containing success value or error message
            
        Raises:
            ValueError: If parameter is invalid
        """
        pass
```

### **README Updates**
When adding new features:
- Update the README.md with new features
- Add usage examples
- Update configuration options
- Update installation instructions

### **API Documentation**
When adding new APIs:
- Document all public methods
- Include parameter descriptions
- Include return value descriptions
- Include usage examples
- Update API documentation

## 🔧 Development Workflow

### **Branch Strategy**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Create bugfix branch
git checkout -b bugfix/fix-issue

# Create hotfix branch
git checkout -b hotfix/critical-fix
```

### **Commit Messages**
Follow conventional commit format:

```bash
# Feature
git commit -m "feat: add new embedding service"

# Bug fix
git commit -m "fix: resolve memory leak in cache service"

# Documentation
git commit -m "docs: update API documentation"

# Test
git commit -m "test: add unit tests for health service"

# Refactor
git commit -m "refactor: improve error handling in ROP service"
```

### **Pull Request Process**
1. **Create Branch**: Create feature branch from main
2. **Implement Changes**: Make your changes
3. **Write Tests**: Add tests for your changes
4. **Update Documentation**: Update relevant documentation
5. **Run Tests**: Ensure all tests pass
6. **Create PR**: Create pull request with description
7. **Code Review**: Address review feedback
8. **Merge**: Merge after approval

## 🎯 Code Style

### **Python Style**
Follow PEP 8 and use Black for formatting:

```bash
# Install Black
pip install black

# Format code
black .

# Check formatting
black --check .
```

### **Import Organization**
```python
# Standard library imports
import os
import sys
from typing import List, Dict, Any

# Third-party imports
import httpx
import pytest

# Local imports
from domain.entities.rag_chunk import RAGChunk
from domain.utils.result import Result
from infrastructure.ai.embeddings.base_embedding_service import BaseEmbeddingService
```

### **Type Hints**
Use type hints for all public methods:

```python
async def create_embedding(self, text: str) -> Result[List[float], str]:
    """Create embedding for text."""
    pass
```

## 🔍 Code Review Guidelines

### **Review Checklist**
- [ ] **Functionality**: Does the code work as intended?
- [ ] **Tests**: Are there adequate tests?
- [ ] **Documentation**: Is documentation updated?
- [ ] **Style**: Does code follow style guidelines?
- [ ] **Architecture**: Does it follow Clean Architecture?
- [ ] **Performance**: Are there performance implications?
- [ ] **Security**: Are there security considerations?

### **Review Process**
1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: At least one reviewer required
3. **Testing**: Reviewer tests the changes
4. **Approval**: Approve after all checks pass
5. **Merge**: Merge to main branch

## 🚨 Issue Guidelines

### **Bug Reports**
Use the bug report template:

```markdown
## Bug Description
Brief description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: [e.g. Windows 10]
- Python Version: [e.g. 3.11]
- Dependencies: [e.g. requirements.txt]

## Additional Context
Any other context about the problem.
```

### **Feature Requests**
Use the feature request template:

```markdown
## Feature Description
Brief description of the feature.

## Use Case
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives
Other solutions considered.

## Additional Context
Any other relevant information.
```

## 📊 Performance Guidelines

### **Performance Considerations**
- **Memory Usage**: Monitor memory consumption
- **Response Time**: Keep response times reasonable
- **Scalability**: Design for horizontal scaling
- **Caching**: Use caching where appropriate

### **Performance Testing**
```python
@pytest.mark.asyncio
async def test_performance():
    """Test service performance."""
    service = ServiceName()
    
    start_time = time.time()
    result = await service.operation()
    response_time = (time.time() - start_time) * 1000
    
    assert result.is_success
    assert response_time < 1000  # Less than 1 second
```

## 🔒 Security Guidelines

### **Security Considerations**
- **Input Validation**: Validate all inputs
- **Authentication**: Implement proper authentication
- **Authorization**: Implement proper authorization
- **Data Protection**: Protect sensitive data
- **Logging**: Log security events

### **Security Testing**
```python
@pytest.mark.asyncio
async def test_security():
    """Test security measures."""
    service = ServiceName()
    
    # Test input validation
    result = await service.operation("")
    assert result.is_error
    
    # Test authentication
    result = await service.operation("valid_input", token="invalid")
    assert result.is_error
```

## 📈 Monitoring Guidelines

### **Health Checks**
Implement health checks for all services:

```python
async def health_check(self) -> Result[HealthCheck, str]:
    """Perform health check."""
    try:
        # Health check logic
        return Result.success(HealthCheck(
            service_name=self.service_name,
            status=HealthStatus.HEALTHY,
            message="Service is healthy"
        ))
    except Exception as e:
        return Result.error(f"Health check failed: {str(e)}")
```

### **Logging**
Use structured logging:

```python
import logging
from infrastructure.monitoring.logging.structured_logger import StructuredLogger

logger = StructuredLogger("service-name")
logger.info("Operation completed", extra={
    "operation": "create_embedding",
    "duration_ms": 150.5,
    "success": True
})
```

## 🎉 Recognition

### **Contributor Recognition**
Contributors will be recognized in:
- **README.md**: Contributor list
- **CHANGELOG.md**: Contribution history
- **GitHub**: Contributor statistics
- **Documentation**: Code attribution

### **Contributor Levels**
- **Contributor**: First contribution
- **Regular Contributor**: Multiple contributions
- **Core Contributor**: Significant contributions
- **Maintainer**: Project maintenance

## 📞 Support

### **Getting Help**
- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For general questions and discussions
- **Documentation**: Check existing documentation
- **Code Review**: Ask questions during code review

### **Community Guidelines**
- **Be Respectful**: Treat everyone with respect
- **Be Constructive**: Provide constructive feedback
- **Be Patient**: Be patient with responses
- **Be Helpful**: Help others when possible

---

**Thank you for contributing to the AI Agent Starter Pack! Your contributions help make this project better for everyone.**

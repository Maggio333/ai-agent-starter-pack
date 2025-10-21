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
git clone https://github.com/Maggio333/ai-agent-starter-pack.git
cd ai-agent-starter-pack

# Add upstream remote
git remote add upstream https://github.com/Maggio333/ai-agent-starter-pack.git
```

### **Development Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📋 Contribution Guidelines

### **Code Standards**
- **Follow Architecture**: Maintain Clean Architecture principles
- **Use Type Hints**: All functions should have type annotations
- **Write Tests**: New features must include tests
- **Document Code**: Add docstrings to all public methods
- **Follow Naming**: Use descriptive names for variables and functions

### **Architecture Guidelines**
- **Clean Architecture**: Follow the established layer separation
- **Dependency Injection**: Use the DI container for service registration
- **Railway Oriented Programming**: Use Result pattern for error handling
- **Interface Segregation**: Create focused interfaces

### **Pull Request Process**
1. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
2. **Make Changes**: Implement your feature with tests
3. **Run Tests**: Ensure all tests pass
4. **Update Documentation**: Update relevant documentation
5. **Submit PR**: Create pull request with clear description

## 🧪 Testing Requirements

### **Test Coverage**
- **Unit Tests**: Test individual components
- **Integration Tests**: Test service interactions
- **End-to-End Tests**: Test complete workflows

### **Running Tests**
```bash
# All tests
python -m pytest tests/

# Specific test file
python -m pytest tests/test_voice_service.py

# With coverage
python -m pytest --cov=application tests/
```

## 📚 Documentation

### **Documentation Standards**
- **User Guides**: Write for non-technical users
- **Developer Guides**: Include code examples
- **API Documentation**: Document all endpoints
- **Architecture**: Explain design decisions

### **Documentation Updates**
- Update relevant documentation with new features
- Include examples and use cases
- Keep documentation current with code changes

## 🐛 Bug Reports

### **Bug Report Template**
```markdown
**Bug Description**
Brief description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9]
- Browser: [e.g., Chrome 91]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

### **Feature Request Template**
```markdown
**Feature Description**
Brief description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives**
Any alternative solutions considered?

**Additional Context**
Any other relevant information
```

## 🏷️ Release Process

### **Version Numbering**
- **Major**: Breaking changes
- **Minor**: New features
- **Patch**: Bug fixes

### **Release Checklist**
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Release notes prepared

## 📞 Support

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **LinkedIn**: [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **GitHub**: [Maggio333](https://github.com/Maggio333)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Thank you for contributing to the AI Agent Starter Pack!** 🎉
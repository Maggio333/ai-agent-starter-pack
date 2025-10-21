# Testing Documentation

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 🧪 Testing Strategy

This project follows a comprehensive testing strategy with multiple levels of testing:

- **Unit Tests**: Individual service and component testing
- **Integration Tests**: Service interaction testing
- **End-to-End Tests**: Complete workflow testing
- **Performance Tests**: Load and stress testing

## 🏗️ Test Structure

```
tests/
├── unit/                      # Unit tests
│   ├── services/              # Service tests
│   ├── domain/                # Domain tests
│   └── infrastructure/        # Infrastructure tests
├── integration/               # Integration tests
├── e2e/                       # End-to-end tests
└── examples/                  # Example usage tests
```

## 🚀 Running Tests

### **All Tests**
```bash
python -m pytest tests/
```

### **Specific Test Categories**
```bash
# Unit tests only
python -m pytest tests/unit/

# Integration tests only
python -m pytest tests/integration/

# End-to-end tests only
python -m pytest tests/e2e/
```

### **With Coverage**
```bash
python -m pytest --cov=application tests/
```

## 📝 Writing Tests

### **Unit Test Example**
```python
import pytest
from application.services.voice_service import VoiceService

class TestVoiceService:
    def test_transcribe_audio_success(self):
        """Test successful audio transcription."""
        # Arrange
        voice_service = VoiceService()
        audio_data = b"fake_audio_data"
        
        # Act
        result = await voice_service.transcribe_audio(audio_data)
        
        # Assert
        assert result.is_success
        assert isinstance(result.value, str)
```

### **Integration Test Example**
```python
import pytest
from application.container import Container

class TestServiceIntegration:
    def test_voice_to_text_workflow(self):
        """Test complete voice-to-text workflow."""
        # Arrange
        container = Container()
        voice_service = container.voice_service()
        llm_service = container.llm_service()
        
        # Act
        audio_result = await voice_service.transcribe_audio(audio_data)
        if audio_result.is_success:
            text_result = await llm_service.generate_response(audio_result.value)
        
        # Assert
        assert audio_result.is_success
        assert text_result.is_success
```

## 🔧 Test Configuration

### **pytest.ini**
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### **Test Dependencies**
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov
```

## 📊 Coverage Requirements

- **Minimum Coverage**: 80%
- **Critical Services**: 90%
- **New Features**: 100%

### **Coverage Report**
```bash
python -m pytest --cov=application --cov-report=html tests/
```

## 🚨 Test Failures

### **Common Issues**
- **Import Errors**: Check PYTHONPATH
- **Async Issues**: Use pytest-asyncio
- **Service Dependencies**: Mock external services

### **Debugging Tests**
```bash
# Run with verbose output
python -m pytest -v tests/

# Run specific test with debugging
python -m pytest -s tests/test_voice_service.py::test_transcribe_audio
```

## 📚 Test Examples

### **Service Tests**
```python
# Test service initialization
def test_service_initialization():
    service = MyService()
    assert service is not None

# Test service methods
def test_service_method():
    service = MyService()
    result = await service.process_data("test")
    assert result.is_success
```

### **Error Handling Tests**
```python
# Test error scenarios
def test_service_error_handling():
    service = MyService()
    result = await service.process_data(None)
    assert result.is_failure
    assert "error" in result.error.lower()
```

## 🎯 Best Practices

### **Test Naming**
- Use descriptive test names
- Follow pattern: `test_<method>_<scenario>`
- Group related tests in classes

### **Test Organization**
- One test file per service
- Separate unit and integration tests
- Use fixtures for common setup

### **Test Data**
- Use realistic test data
- Avoid hardcoded values
- Use factories for complex objects

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues
- **LinkedIn**: [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **GitHub**: [Maggio333](https://github.com/Maggio333)

---

**Happy Testing!** 🧪✨
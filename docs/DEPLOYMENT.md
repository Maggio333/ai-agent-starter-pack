# Deployment Documentation

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 🚀 Deployment Overview

This document covers deployment strategies for the AI Agent Starter Pack, including local development, containerization, and cloud deployment options.

## 🏠 Local Development

### **Prerequisites**
```bash
# Python 3.8+
python --version

# Virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt
```

### **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
# EMBEDDING_PROVIDER=lmstudio
# LMSTUDIO_PROXY_URL=http://127.0.0.1:8123
# QDRANT_URL=http://localhost:6333
```

### **External Services**
```bash
# Start Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

# Start LM Studio (Local)
# Launch LM Studio and start embedding model
# Configure proxy at http://127.0.0.1:8123
```

### **Run Application**
```bash
# Start main application
python main.py

# Run tests
python -m pytest tests/

# Run specific service
python tests/test_health_service.py
```

## 🐳 Docker Deployment

### **Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start application
CMD ["python", "main.py"]
```

### **Docker Compose**
```yaml
version: '3.8'

services:
  ai-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - EMBEDDING_PROVIDER=lmstudio
      - LMSTUDIO_PROXY_URL=http://lmstudio:8123
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - qdrant
      - lmstudio
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  lmstudio:
    image: lmstudio/lmstudio:latest
    ports:
      - "8123:8123"
    volumes:
      - lmstudio_data:/app/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  qdrant_data:
  lmstudio_data:
  redis_data:
```

### **Build and Run**
```bash
# Build image
docker build -t ai-agent-starter-pack .

# Run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f ai-agent

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment

### **Google Cloud Platform**

#### **Cloud Run**
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ai-agent', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/ai-agent']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'ai-agent', '--image', 'gcr.io/$PROJECT_ID/ai-agent', '--platform', 'managed', '--region', 'us-central1']
```

#### **Terraform Configuration**
```hcl
# main.tf
resource "google_cloud_run_service" "ai_agent" {
  name     = "ai-agent"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/ai-agent"
        
        env {
          name  = "EMBEDDING_PROVIDER"
          value = "google"
        }
        
        env {
          name  = "GOOGLE_PROJECT_ID"
          value = var.project_id
        }
        
        env {
          name  = "QDRANT_URL"
          value = "https://qdrant.example.com"
        }
      }
    }
  }
}
```

### **AWS Deployment**

#### **ECS Task Definition**
```json
{
  "family": "ai-agent",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ai-agent",
      "image": "your-account.dkr.ecr.region.amazonaws.com/ai-agent:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "EMBEDDING_PROVIDER",
          "value": "huggingface"
        },
        {
          "name": "HUGGINGFACE_API_TOKEN",
          "value": "your-token"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-agent",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### **Azure Deployment**

#### **Container Instances**
```yaml
# azure-deployment.yaml
apiVersion: 2021-07-01
location: eastus
name: ai-agent
properties:
  containers:
  - name: ai-agent
    properties:
      image: your-registry.azurecr.io/ai-agent:latest
      ports:
      - port: 8000
      environmentVariables:
      - name: EMBEDDING_PROVIDER
        value: "openai"
      - name: OPENAI_API_KEY
        secureValue: "your-openai-key"
      resources:
        requests:
          cpu: 1.0
          memoryInGb: 2.0
  osType: Linux
  restartPolicy: Always
```

## 🔧 Configuration Management

### **Environment Variables**
```bash
# Production environment
export EMBEDDING_PROVIDER=google
export GOOGLE_PROJECT_ID=your-project
export GOOGLE_API_KEY=your-key
export QDRANT_URL=https://qdrant.example.com
export CACHE_PROVIDER=redis
export REDIS_URL=redis://redis.example.com:6379
export LOG_LEVEL=INFO
export DEBUG=false
```

### **Secrets Management**
```bash
# Google Secret Manager
gcloud secrets create embedding-api-key --data-file=key.txt

# AWS Secrets Manager
aws secretsmanager create-secret --name "ai-agent/api-keys" --secret-string '{"openai":"key","huggingface":"token"}'

# Azure Key Vault
az keyvault secret set --vault-name "ai-agent-vault" --name "api-keys" --value '{"openai":"key"}'
```

## 📊 Monitoring and Logging

### **Health Checks**
```python
# Health check endpoint
@app.get("/health")
async def health_check():
    health_service = container.health_service()
    result = await health_service.get_overall_health()
    
    if result.is_success:
        return {"status": "healthy", "details": result.value}
    else:
        return {"status": "unhealthy", "error": result.error}
```

### **Logging Configuration**
```python
# Structured logging
import logging
from infrastructure.monitoring.logging.structured_logger import StructuredLogger

logger = StructuredLogger("ai-agent")
logger.info("Application started", extra={
    "service": "ai-agent",
    "version": "1.0.0",
    "environment": "production"
})
```

### **Metrics Collection**
```python
# Prometheus metrics (planned)
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@REQUEST_DURATION.time()
async def process_request():
    REQUEST_COUNT.inc()
    # Process request
```

## 🔒 Security Considerations

### **Network Security**
```yaml
# Docker network
networks:
  ai-agent-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### **SSL/TLS**
```nginx
# Nginx configuration
server {
    listen 443 ssl;
    server_name ai-agent.example.com;
    
    ssl_certificate /etc/ssl/certs/ai-agent.crt;
    ssl_certificate_key /etc/ssl/private/ai-agent.key;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Authentication**
```python
# JWT authentication (planned)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    # Verify JWT token
    if not is_valid_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token
```

## 📈 Scaling Strategies

### **Horizontal Scaling**
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-agent
  template:
    metadata:
      labels:
        app: ai-agent
    spec:
      containers:
      - name: ai-agent
        image: ai-agent:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### **Load Balancing**
```yaml
# Kubernetes service
apiVersion: v1
kind: Service
metadata:
  name: ai-agent-service
spec:
  selector:
    app: ai-agent
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### **Auto-scaling**
```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 🔄 CI/CD Pipeline

### **GitHub Actions**
```yaml
# .github/workflows/deploy.yml
name: Deploy AI Agent

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-asyncio
    - name: Run tests
      run: python -m pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: docker build -t ai-agent .
    - name: Push to registry
      run: docker push your-registry/ai-agent:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        # Deployment commands
        kubectl apply -f k8s/
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Service Not Starting**
```bash
# Check logs
docker logs ai-agent

# Check health
curl http://localhost:8000/health

# Check dependencies
docker ps | grep qdrant
docker ps | grep redis
```

#### **Memory Issues**
```bash
# Check memory usage
docker stats ai-agent

# Increase memory limits
docker run --memory=2g ai-agent
```

#### **Network Issues**
```bash
# Check network connectivity
docker exec ai-agent ping qdrant
docker exec ai-agent curl http://qdrant:6333/health
```

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export DEBUG=true

# Run with debug
python main.py --debug
```

## 📋 Deployment Checklist

### **Pre-deployment**
- [ ] Tests passing
- [ ] Environment variables configured
- [ ] Secrets managed securely
- [ ] Monitoring configured
- [ ] Health checks implemented

### **Deployment**
- [ ] Build successful
- [ ] Image pushed to registry
- [ ] Services deployed
- [ ] Health checks passing
- [ ] Monitoring active

### **Post-deployment**
- [ ] Smoke tests passing
- [ ] Performance metrics normal
- [ ] Logs being collected
- [ ] Alerts configured
- [ ] Documentation updated

---

**For more deployment examples and configurations, see the `deployment/` directory.**

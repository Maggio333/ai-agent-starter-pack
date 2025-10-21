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

# Install dependencies
pip install -r requirements.txt
```

### **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
# LMSTUDIO_LLM_PROXY_URL=http://127.0.0.1:8123
# EMBEDDING_PROVIDER=lmstudio
```

### **Run Application**
```bash
# Start backend
python main.py

# Start Flutter UI (optional)
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```

## 🐳 Docker Deployment

### **Dockerfile**
```dockerfile
FROM python:3.9-slim

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

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "main.py"]
```

### **Docker Compose**
```yaml
version: '3.8'

services:
  ai-agent:
    build: .
    ports:
      - "8080:8080"
    environment:
      - LMSTUDIO_LLM_PROXY_URL=http://lmstudio:8123
    depends_on:
      - lmstudio

  lmstudio:
    image: lmstudio/lmstudio:latest
    ports:
      - "8123:8123"
    volumes:
      - ./models:/models
```

### **Build and Run**
```bash
# Build image
docker build -t ai-agent-starter-pack .

# Run container
docker run -p 8080:8080 ai-agent-starter-pack

# Or use docker-compose
docker-compose up -d
```

## ☁️ Cloud Deployment

### **Google Cloud Run**
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-agent-starter-pack

# Deploy to Cloud Run
gcloud run deploy ai-agent-starter-pack \
  --image gcr.io/PROJECT_ID/ai-agent-starter-pack \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### **AWS ECS**
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t ai-agent-starter-pack .
docker tag ai-agent-starter-pack:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-agent-starter-pack:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-agent-starter-pack:latest
```

### **Azure Container Instances**
```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image ai-agent-starter-pack .

# Deploy to Container Instances
az container create \
  --resource-group myResourceGroup \
  --name ai-agent-starter-pack \
  --image myregistry.azurecr.io/ai-agent-starter-pack:latest \
  --ports 8080
```

## 🔧 Production Configuration

### **Environment Variables**
```bash
# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
PORT=8080

# AI Services
LMSTUDIO_LLM_PROXY_URL=http://lmstudio:8123
EMBEDDING_PROVIDER=lmstudio

# Database
DATABASE_URL=postgresql://user:pass@db:5432/ai_agent

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

### **Health Checks**
```python
# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "llm": await check_llm_service(),
            "voice": await check_voice_service(),
            "database": await check_database()
        }
    }
```

## 📊 Monitoring

### **Logging Configuration**
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### **Metrics Collection**
```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Use in endpoints
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    REQUEST_COUNT.inc()
    REQUEST_DURATION.observe(process_time)
    
    return response
```

## 🔒 Security

### **HTTPS Configuration**
```python
# Use HTTPS in production
if ENVIRONMENT == "production":
    import ssl
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('cert.pem', 'key.pem')
    
    uvicorn.run(app, ssl_context=ssl_context)
```

### **Authentication**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    # Verify JWT token
    if not verify_jwt_token(token.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return token
```

## 📈 Scaling

### **Horizontal Scaling**
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-starter-pack
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-agent-starter-pack
  template:
    metadata:
      labels:
        app: ai-agent-starter-pack
    spec:
      containers:
      - name: ai-agent-starter-pack
        image: ai-agent-starter-pack:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### **Load Balancing**
```nginx
# Nginx configuration
upstream ai_agent {
    server ai-agent-1:8080;
    server ai-agent-2:8080;
    server ai-agent-3:8080;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://ai_agent;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🚨 Troubleshooting

### **Common Issues**
- **Port Conflicts**: Check if port 8080 is available
- **Memory Issues**: Increase container memory limits
- **Database Connection**: Verify database URL and credentials
- **Service Dependencies**: Ensure all services are running

### **Debug Commands**
```bash
# Check container logs
docker logs ai-agent-starter-pack

# Check service health
curl http://localhost:8080/health

# Check resource usage
docker stats ai-agent-starter-pack
```

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues
- **LinkedIn**: [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **GitHub**: [Maggio333](https://github.com/Maggio333)

---

**Happy Deploying!** 🚀✨
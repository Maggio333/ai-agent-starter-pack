# Docker Setup Guide - AI Agent Starter Pack

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 📋 Overview

This guide explains how to use Docker and Docker Compose to run the AI Agent Starter Pack in a containerized environment.

## 🐳 Prerequisites

- **Docker** 20.10+ installed
- **Docker Compose** 2.0+ installed
- At least **4GB RAM** available
- **10GB free disk space** for images and volumes

### Installation

#### Windows:
```powershell
# Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

#### Linux:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## 🚀 Quick Start

### 1. Prepare Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
# At minimum, set:
# - API_PORT=8080
# - LLM_PROVIDER=lmstudio
# - EMBEDDING_PROVIDER=lmstudio
```

### 2. Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 3. Setup LM Studio (if using LM Studio provider)

**⚠️ Important**: LM Studio must be running on your host machine before starting Docker containers.

```bash
# 1. Install LM Studio from https://lmstudio.ai/
# 2. Start LM Studio application
# 3. Load a model in LM Studio
# 4. Start Local Server in LM Studio (Settings → Local Server)
#    - Port: 8123
#    - Make sure it's running before starting Docker
```

### 4. Access Services

- **Frontend (Flutter UI)**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs
- **Qdrant UI**: http://localhost:6333/dashboard
- **LM Studio**: http://localhost:8123 (must be running on host)

### 5. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v
```

## 📦 Services

### Flutter Voice UI Frontend

Flutter Web frontend application served by nginx.

**Port**: 3000 (configurable via `FRONTEND_PORT`)  
**Health Check**: http://localhost:3000/health  
**URL**: http://localhost:3000

**Features**:
- Served by nginx with reverse proxy to backend
- API requests (`/api/*`) are proxied to `ai-agent-backend:8080`
- Static files (`/static/*`) are proxied to backend
- Optimized caching for static assets
- CORS headers configured for API access

**Build**: Multi-stage Docker build (Flutter build + nginx serve)

### AI Agent Backend

Main FastAPI application.

**Port**: 8080  
**Health Check**: http://localhost:8080/api/health

### Qdrant Vector Database

Vector database for embeddings and RAG.

**Port**: 6333 (HTTP), 6334 (gRPC)  
**Dashboard**: http://localhost:6333/dashboard

### LM Studio

Local LLM and embedding service.

**Port**: 8123  
**⚠️ Important**: LM Studio does NOT run in Docker. It must be installed and running on your host machine.

**Setup**:
1. Install LM Studio from https://lmstudio.ai/
2. Start LM Studio on your host machine
3. Start a local server in LM Studio on port 8123
4. The Docker container will connect to it via `host.docker.internal:8123`

**Alternative**: Use Ollama (has Docker image) or cloud providers (Google, OpenAI)

### Redis (Optional)

Caching service. Only starts with `--profile cache`.

```bash
docker-compose --profile cache up
```

### Ollama (Optional)

Alternative LLM provider. Only starts with `--profile ollama`.

```bash
docker-compose --profile ollama up
```

## 🔧 Configuration

### Environment Variables

All configuration is done through `.env` file. See `env.example` for all available options.

### Key Variables:

```bash
# Application
API_PORT=8080
FRONTEND_PORT=3000
DEBUG=false
LOG_LEVEL=INFO

# LLM
LLM_PROVIDER=lmstudio
# For Docker: use host.docker.internal to connect to LM Studio on host
LMSTUDIO_LLM_PROXY_URL=http://host.docker.internal:8123

# Embeddings
EMBEDDING_PROVIDER=lmstudio
# For Docker: use host.docker.internal to connect to LM Studio on host
LMSTUDIO_PROXY_URL=http://host.docker.internal:8123

# Vector DB
VECTOR_DB_PROVIDER=qdrant
QDRANT_URL=http://qdrant:6333
```

### Volumes

Data persistence is handled through Docker volumes:

- `qdrant_data` - Qdrant database storage
- `lmstudio_models` - LM Studio model files
- `./data` - Application data (mounted from host)
- `./static` - Static files (mounted from host)
- `./voices` - Voice model files (mounted from host)

## 🛠️ Development

### Development Mode

For development with hot-reload:

```bash
# Override CMD in docker-compose
docker-compose run --rm -p 8080:8080 \
  -e RELOAD=true \
  ai-agent-backend \
  uvicorn main_fastapi:app --reload --host 0.0.0.0 --port 8080
```

### Building Custom Image

```bash
# Build image
docker build -t ai-agent-starter-pack:latest .

# Run container
docker run -p 8080:8080 \
  --env-file .env \
  ai-agent-starter-pack:latest
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ai-agent-backend

# Last 100 lines
docker-compose logs --tail=100 ai-agent-backend
```

## 🧪 Testing

### Run Tests in Container

```bash
# Run all tests
docker-compose run --rm ai-agent-backend pytest tests/ -v

# Run specific test
docker-compose run --rm ai-agent-backend pytest tests/test_endpoint.py -v
```

## 🔍 Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8080

# Linux:
lsof -i :8080

# Change port in .env
API_PORT=8081
```

### Container Won't Start

```bash
# Check logs
docker-compose logs ai-agent-backend

# Check container status
docker-compose ps

# Restart service
docker-compose restart ai-agent-backend
```

### Qdrant Connection Issues

```bash
# Check Qdrant health
curl http://localhost:6333/health

# Check Qdrant logs
docker-compose logs qdrant

# Restart Qdrant
docker-compose restart qdrant
```

### LM Studio Connection Issues

**Problem**: Backend cannot connect to LM Studio

**Solutions**:

1. **Verify LM Studio is running on host**:
   ```bash
   # Check if LM Studio is running
   # Windows: Check Task Manager
   # Linux/Mac: ps aux | grep lmstudio
   ```

2. **Verify LM Studio server is started**:
   - Open LM Studio
   - Go to Settings → Local Server
   - Make sure server is running on port 8123
   - Check "Allow connections from localhost"

3. **Test connection from host**:
   ```bash
   # Test if LM Studio responds
   curl http://localhost:8123/v1/models
   ```

4. **Check Docker network**:
   ```bash
   # Verify host.docker.internal is accessible
   docker-compose exec ai-agent-backend ping host.docker.internal
   ```

5. **Alternative: Use Ollama instead**:
   ```bash
   # Start Ollama
   docker-compose --profile ollama up -d ollama
   
   # Update .env
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://ollama:11434
   ```

### Out of Memory

```bash
# Check memory usage
docker stats

# Increase Docker memory limit in Docker Desktop settings
# Or reduce services:
docker-compose up ai-agent-backend qdrant
```

### Database Locked (SQLite)

If using SQLite and getting "database is locked" errors:

```bash
# Stop all containers
docker-compose down

# Remove database file (⚠️ deletes data)
rm data/chat.db

# Restart
docker-compose up
```

## 📊 Monitoring

### Health Checks

All services have health checks configured:

```bash
# Check backend health
curl http://localhost:8080/api/health

# Check Qdrant health
curl http://localhost:6333/health

# Check Redis health
docker-compose exec redis redis-cli ping
```

### Metrics

If `ENABLE_METRICS=true`:

```bash
# Access metrics endpoint
curl http://localhost:9090/metrics
```

## 🚀 Production Deployment

### Security Considerations

1. **Change default secrets** in `.env`:
   ```bash
   SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   ENCRYPTION_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   ```

2. **Use secrets management**:
   ```yaml
   # docker-compose.yml
   secrets:
     - secret_key
     - jwt_secret
   ```

3. **Limit exposed ports**:
   - Only expose necessary ports
   - Use reverse proxy (nginx, traefik)

4. **Use production images**:
   ```dockerfile
   FROM python:3.10-slim
   # ... production optimizations
   ```

### Scaling

```bash
# Scale backend service
docker-compose up -d --scale ai-agent-backend=3

# Use load balancer (nginx, traefik)
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

**Last Updated**: 2025-11-11  
**Version**: 1.2.0


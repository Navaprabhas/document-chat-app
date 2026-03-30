# 🚀 Deployment Guide

Complete guide for deploying the Document Chat Application to production.

## 📋 Pre-Deployment Checklist

- [ ] All tests pass (`python test_setup.py`)
- [ ] Environment variables configured
- [ ] API keys secured (not in code)
- [ ] Dependencies locked (`pip freeze > requirements.txt`)
- [ ] Error handling tested
- [ ] Logging configured
- [ ] Rate limiting considered
- [ ] Security review completed

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Easiest)

**Pros**: Free tier, automatic HTTPS, easy setup
**Cons**: Limited resources, public by default

#### Steps:

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
- Go to https://share.streamlit.io
- Click "New app"
- Select your repository
- Set main file: `app.py`
- Add secrets in "Advanced settings"

3. **Configure Secrets**
In Streamlit Cloud dashboard, add:
```toml
OPENAI_API_KEY = "sk-your-key-here"
LLM_PROVIDER = "openai"
OPENAI_MODEL = "gpt-4-turbo-preview"
```

4. **Deploy**
- Click "Deploy"
- Wait 2-3 minutes
- Your app is live!

### Option 2: Docker (Recommended for Production)

**Pros**: Portable, consistent, scalable
**Cons**: Requires Docker knowledge

#### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p temp chroma_db logs

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  document-chat:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LLM_PROVIDER=${LLM_PROVIDER}
      - OPENAI_MODEL=${OPENAI_MODEL}
    volumes:
      - ./chroma_db:/app/chroma_db
      - ./logs:/app/logs
    restart: unless-stopped
```

#### Deploy with Docker

```bash
# Build image
docker build -t document-chat .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-key \
  -v $(pwd)/chroma_db:/app/chroma_db \
  document-chat

# Or use docker-compose
docker-compose up -d
```

### Option 3: AWS EC2

**Pros**: Full control, scalable
**Cons**: More complex, costs money

#### Steps:

1. **Launch EC2 Instance**
- Ubuntu 22.04 LTS
- t3.medium or larger
- Open port 8501 in security group

2. **SSH and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone <your-repo-url>
cd document-chat-app

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

3. **Run with systemd**

Create `/etc/systemd/system/document-chat.service`:
```ini
[Unit]
Description=Document Chat Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/document-chat-app
Environment="PATH=/home/ubuntu/document-chat-app/venv/bin"
ExecStart=/home/ubuntu/document-chat-app/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable document-chat
sudo systemctl start document-chat
```

4. **Setup Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Option 4: Heroku

**Pros**: Easy deployment, free tier
**Cons**: Limited resources, cold starts

#### Files needed:

**Procfile**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt**
```
python-3.10.12
```

#### Deploy:
```bash
heroku login
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

## 🔒 Security Best Practices

### 1. Environment Variables
```python
# Never hardcode secrets
# ❌ BAD
OPENAI_API_KEY = "sk-abc123..."

# ✅ GOOD
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 2. Input Validation
```python
# Add to app.py
def validate_file(uploaded_file):
    # Check file size
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        raise ValueError("File too large")
    
    # Check file type
    if not uploaded_file.name.endswith('.pdf'):
        raise ValueError("Only PDF files allowed")
    
    return True
```

### 3. Rate Limiting
```python
# Add to config.py
MAX_REQUESTS_PER_MINUTE = 10
MAX_DOCUMENTS_PER_USER = 5
```

### 4. Authentication (Optional)
```python
# Add to app.py
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    'document_chat',
    'auth_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show app
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

## 📊 Monitoring

### Application Logs
```python
# Enhanced logging in config.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10000000,
    backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler]
)
```

### Health Check Endpoint
```python
# Add to app.py
@st.cache_resource
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

### Metrics to Track
- Request count
- Response time
- Error rate
- API costs
- Document processing time
- Vector store size

## 💰 Cost Optimization

### OpenAI API Costs
```python
# Use cheaper models for embeddings
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # Cheaper

# Cache embeddings
@st.cache_data
def get_embeddings(text):
    return embeddings.embed_query(text)

# Limit context size
MAX_TOKENS = 1000  # Reduce from 2000
```

### Infrastructure Costs
- Use spot instances on AWS
- Auto-scaling based on traffic
- CDN for static assets
- Compress vector store

## 🔧 Performance Optimization

### 1. Caching
```python
@st.cache_resource
def load_embeddings_manager():
    return EmbeddingsManager()

@st.cache_data
def process_document(file_path):
    return DocumentProcessor().process_pdf(file_path)
```

### 2. Async Processing
```python
import asyncio

async def process_multiple_documents(files):
    tasks = [process_document(f) for f in files]
    return await asyncio.gather(*tasks)
```

### 3. Database Optimization
```python
# Batch insertions
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=documents,
    metadatas=metadatas
)
```

## 🧪 Testing in Production

### Load Testing
```bash
# Install locust
pip install locust

# Create locustfile.py
# Run load test
locust -f locustfile.py --host=http://your-app-url
```

### Smoke Tests
```bash
# Test health endpoint
curl http://your-app-url/_stcore/health

# Test document upload
# (manual test in browser)
```

## 📱 Mobile Optimization

```python
# Add to app.py CSS
st.markdown("""
<style>
@media (max-width: 768px) {
    .main-header {
        font-size: 1.5rem;
    }
    .sidebar .sidebar-content {
        width: 100%;
    }
}
</style>
""", unsafe_allow_html=True)
```

## 🔄 CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit Cloud
        run: |
          # Your deployment script
```

## 📞 Support & Maintenance

### Backup Strategy
- Daily vector store backups
- Weekly full backups
- Keep 30 days of backups

### Update Process
1. Test in staging
2. Deploy during low-traffic hours
3. Monitor for errors
4. Rollback if needed

### Monitoring Alerts
- Set up alerts for:
  - High error rates
  - Slow response times
  - API quota exceeded
  - Disk space low

---

**Need help?** Check the main README.md or create an issue on GitHub.

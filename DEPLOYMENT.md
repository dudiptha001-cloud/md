# Deployment Guide - Customer Support Agent

This guide covers deploying the Customer Support Agent to different platforms and environments.

---

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Cloud Platforms](#cloud-platforms)
3. [Production Considerations](#production-considerations)
4. [Monitoring & Scale](#monitoring--scale)

---

## Local Deployment

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Installation Steps

#### 1. Clone/Download the Project
```bash
cd C:\Users\dudip\Customer Support Agent — End-to-End Pipeline
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure API Keys
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your keys:
# OPENAI_API_KEY=sk-...
# DEMO_MODE=False  (to use real AI)
```

#### 5. Run the Application
```bash
streamlit run app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

### Access the App
- Open browser to `http://localhost:8501`
- Chat interface loads immediately
- Upload documents to build knowledge base
- Test with sample questions

---

## Cloud Platforms

### Option 1: Streamlit Cloud (Easiest)

**Pros:**
- Free tier available
- One-click deployment from GitHub
- Automatic scaling
- Built-in monitoring

**Cons:**
- Limited to 1GB memory
- ~2-3 second cold start
- Streamlit-hosted (subdomains only)

#### Steps:

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/support-agent.git
git push -u origin main
```

2. **Connect to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Select repository: `yourusername/support-agent`
   - Select branch: `main`
   - Select file: `app.py`

3. **Add Secrets**
   - In Streamlit Cloud dashboard, go to "Advanced settings"
   - Add secrets (instead of `.env`):
   ```
   OPENAI_API_KEY = "sk-..."
   USE_AZURE = false
   DEMO_MODE = false
   ```

4. **Deploy**
   - Click "Deploy"
   - App runs at `https://yourusername-support-agent.streamlit.app`

**Cost:**
- Free tier: 1 app, up to 500 hours/month
- Pro tier: $9/month per seat for more apps

---

### Option 2: Heroku (Flexible)

**Pros:**
- Full server control
- Better performance
- Custom domain support
- Can add databases

**Cons:**
- Free tier shutdown (Oct 2022)
- Paid plans start at $7/month
- Need Procfile configuration

#### Steps:

1. **Create Procfile**
```bash
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

2. **Create .streamlitrc**
```bash
mkdir -p ~/.streamlit
cat > /app/.streamlit/config.toml << EOF
[browser]
gatherUsageStats = false

[server]
headless = true
runOnSave = true
port = 8501
EOF
```

3. **Create requirements.txt**
```bash
pip freeze > requirements.txt
```

4. **Push to Heroku**
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add environment variables
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set DEMO_MODE=false

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Cost:** $7-25/month depending on dyno size

---

### Option 3: AWS (Enterprise)

**Pros:**
- Enterprise-grade infrastructure
- Unlimited scaling
- Multiple deployment options
- Integration with other AWS services

**Cons:**
- Complex setup
- Cost can escalate
- More configuration needed

#### Deployment Options:

**A. AWS Elastic Beanstalk (Easiest for Streamlit)**

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize Elastic Beanstalk
eb init -p python-3.10 support-agent --region us-east-1

# 3. Create environment
eb create support-agent-env

# 4. Set environment variables
eb setenv OPENAI_API_KEY=sk-... DEMO_MODE=false

# 5. Deploy
git add .
eb deploy

# 6. Open app
eb open
```

**Cost:** ~$10-50/month for small instance

**B. AWS EC2 (More Control)**

```bash
# 1. Launch Ubuntu 20.04 instance
# 2. SSH into instance
ssh -i key.pem ubuntu@ec2-instance.amazonaws.com

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# 4. Clone repository
git clone https://github.com/yourusername/support-agent.git

# 5. Setup and run
cd support-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Run with systemd
sudo systemctl start streamlit

# 7. Setup Nginx reverse proxy
sudo nano /etc/nginx/sites-available/default
# Proxy to port 8501
```

**Cost:** ~$5-100/month depending on instance size

---

### Option 4: Google Cloud Run (Serverless)

**Pros:**
- Pay only for usage
- Automatic scaling
- Built-in monitoring
- Integrates with GCP services

**Cons:**
- Requires Docker
- Cold starts (first request slow)
- Container size limit (~1GB)

#### Steps:

1. **Create Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

2. **Deploy to Cloud Run**
```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT_ID/support-agent

# Deploy
gcloud run deploy support-agent \
  --image gcr.io/PROJECT_ID/support-agent \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-...,DEMO_MODE=false
```

**Cost:** Free tier: 2M requests/month, $0.40 per 1M additional requests

---

### Option 5: Azure App Service

**Pros:**
- Native Azure OpenAI integration
- Enterprise compliance
- Auto-scaling
- Good for enterprises using Azure

**Cons:**
- Requires Azure account
- Setup complexity

#### Steps:

```bash
# 1. Install Azure CLI
# 2. Login
az login

# 3. Create resource group
az group create --name support-agent-rg --location eastus

# 4. Create App Service Plan
az appservice plan create \
  --name support-agent-plan \
  --resource-group support-agent-rg \
  --sku B1 --is-linux

# 5. Deploy
az webapp up \
  --resource-group support-agent-rg \
  --name support-agent-app \
  --runtime "PYTHON:3.10" \
  --src-dir .

# 6. Configure settings
az webapp config appsettings set \
  --resource-group support-agent-rg \
  --name support-agent-app \
  --settings OPENAI_API_KEY=sk-... DEMO_MODE=false
```

**Cost:** $10-100/month depending on tier

---

## Production Considerations

### 1. Security

**API Keys:**
```bash
# ✅ DO: Use environment variables
export OPENAI_API_KEY="sk-..."

# ❌ DON'T: Store in code
api_key = "sk-..."  # NEVER!

# ✅ DO: Use secrets manager
aws secretsmanager create-secret --name support-agent/openai-key
```

**HTTPS:**
```bash
# ✅ All connections must be HTTPS
# Use CloudFlare or Let's Encrypt for free SSL

# ❌ Never expose HTTP
```

**Rate Limiting:**
```python
# Add to app.py to prevent abuse
from streamlit import session_state as ss
import time

if 'last_query_time' not in ss:
    ss.last_query_time = 0

# Rate limit: 1 request per second
elapsed = time.time() - ss.last_query_time
if elapsed < 1:
    st.error(f"Please wait {1-elapsed:.1f}s before next query")
    st.stop()
ss.last_query_time = time.time()
```

### 2. Performance Optimization

**Cache Configurations:**
```python
# In app.py
import streamlit as st

@st.cache_resource
def load_agent():
    """Load agent once, reuse for all requests"""
    return SupportAgent()

agent = load_agent()
```

**Reduce Knowledge Base Size:**
```bash
# Keep only relevant documents
# Remove old/duplicate knowledge base entries
# Archive old docs separately

# Check size
du -sh data/documents/
# Target: < 500MB total
```

**Batch Processing:**
```bash
# For high volume: Queue processing instead of real-time
# Use Celery or AWS Lambda for async tasks
```

### 3. Monitoring

**Logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Query: {question}")
logger.error(f"API Error: {str(e)}")
```

**Error Tracking:**
```bash
# Option 1: Sentry (error monitoring)
pip install sentry-sdk
import sentry_sdk
sentry_sdk.init("https://key@sentry.io/project")

# Option 2: Cloud Logging
from google.cloud import logging as cloud_logging
client = cloud_logging.Client()
client.setup_logging()
```

**Metrics to Track:**
- Query response time (target: <2s)
- API error rate (target: <1%)
- Cost per query (target: $0.10)
- User satisfaction (target: >85%)

### 4. Backup & Recovery

**Knowledge Base Backup:**
```bash
# Daily backup
cp -r data/documents/ backups/documents_$(date +%Y%m%d).tar.gz

# Or use cloud sync
aws s3 sync data/documents/ s3://backup-bucket/documents/
```

**Database Backups:**
```bash
# Backup FAISS index
cp -r data/vectorstore/ backups/vectorstore_$(date +%Y%m%d)/
```

---

## Monitoring & Scale

### Scaling Strategy

**Phase 1: Beta (0-100 users)**
- Streamlit Cloud Free
- Single instance
- Demo mode initially
- Monitor costs

**Phase 2: Growth (100-1K users)**
- Move to AWS EC2 (t3.small)
- Add monitoring (CloudWatch)
- Cache improvements
- Real-time metrics

**Phase 3: Scale (1K-10K users)**
- Kubernetes (EKS/GKE)
- Load balancing
- Database (PostgreSQL)
- CDN for static files

**Phase 4: Enterprise (10K+ users)**
- Multi-region deployment
- Advanced caching
- Custom LLM optimization
- Dedicated support

### Estimated Costs

| Users | Streamlit | AWS | GCP | Azure |
|-------|-----------|-----|-----|-------|
| 0-100 | $0 | $10 | $0 | $10 |
| 100-1K | $10 | $50 | $50 | $50 |
| 1K-10K | $100 | $200 | $150 | $200 |
| 10K+ | $500+ | $1K+ | $800+ | $1K+ |

### Auto-Scaling Configuration

**AWS Elastic Beanstalk:**
```bash
# Set up auto-scaling
eb scale 3  # Start with 3 instances

# Configure auto-scaling rules
# Scale up: CPU > 70% for 2 minutes
# Scale down: CPU < 30% for 5 minutes
```

**Kubernetes:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: support-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: support-agent
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

---

## Quick Start: Recommended Deployment Paths

### For Testing
```bash
# 1. Local machine
streamlit run app.py

# 2. Share with team (ngrok)
pip install pyngrok
ngrok http 8501  # Creates temporary URL
```

### For Small Team (< 50 users)
```bash
# Use Streamlit Cloud
# Go to https://share.streamlit.io/
# Done in 5 minutes
```

### For Growing Use (50-1K users)
```bash
# Deploy to AWS Elastic Beanstalk
# 30 minute setup
# Better performance & control
```

### For Enterprise (1K+ users)
```bash
# Deploy to Kubernetes
# Better scaling & reliability
# Full monitoring suite
```

---

## Troubleshooting Deployment

### Issue: App takes too long to load
**Solution:**
- Enable caching: `@st.cache_resource`
- Reduce knowledge base size
- Use smaller embeddings model

### Issue: API calls timing out
**Solution:**
- Check API rate limits
- Implement request queuing
- Use async processing

### Issue: Memory errors
**Solution:**
- Reduce FAISS index size
- Stream documents instead of loading all
- Use vector database (Weaviate/Milvus) instead of FAISS

### Issue: Can't connect to OpenAI
**Solution:**
- Check API key in environment
- Verify IP whitelist on Azure
- Use demo mode for testing

---

## Next Steps

1. Choose deployment platform
2. Follow platform-specific setup
3. Test with sample questions
4. Add monitoring & logging
5. Set up automatic backups
6. Scale based on usage patterns

For questions, refer to README_COMPLETE.md or QUICKSTART.md

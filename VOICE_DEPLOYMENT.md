# 🗣️ Voice AI Agent - Deployment Guide

This document provides comprehensive deployment instructions for the Voice AI Agent across multiple platforms.

## 🚀 Quick Deploy Options

### 1. Streamlit Community Cloud (Recommended)
**Best for**: Demo and personal use
- Fork this repository on GitHub
- Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/)
- Deploy directly from your repository
- Add `GROQ_API_KEY` in the Streamlit secrets

### 2. Railway (Production Ready)
**Best for**: Production with custom domains
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add
railway deploy
```

### 3. Render (Free Tier Available)
**Best for**: Cost-effective production
- Connect your GitHub repository
- Use `streamlit run streamlit_app.py` as start command
- Add environment variables in Render dashboard

## 🎙️ Voice Features Deployment Notes

### Audio Processing Requirements
The Voice AI Agent includes audio processing capabilities that may require additional system dependencies:

```bash
# For Ubuntu/Debian systems
sudo apt-get update
sudo apt-get install -y ffmpeg libportaudio2 libasound2-dev

# For CentOS/RHEL systems
sudo yum install -y ffmpeg portaudio-devel alsa-lib-devel
```

### Browser Recording Feature
The experimental browser recording feature requires:
- HTTPS connection for microphone access
- Modern browser with WebRTC support
- `streamlit-webrtc` component (included in requirements)

### Environment Variables

#### Required
```bash
GROQ_API_KEY=your_groq_api_key_here
```

#### Optional (for enhanced features)
```bash
# For real speech-to-text integration
OPENAI_API_KEY=your_openai_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_key_here

# For enhanced audio processing
FFMPEG_BINARY_PATH=/usr/bin/ffmpeg
```

## 🐳 Docker Deployment

### Build and Run
```bash
docker build -t voice-ai-agent .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key voice-ai-agent
```

### Docker Compose
```yaml
version: '3.8'
services:
  voice-ai-agent:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./app/vectorstore:/app/vectorstore
    restart: unless-stopped
```

## ☁️ Cloud Platform Specifics

### AWS ECS/Fargate
- Use the provided Dockerfile
- Set up ECS task definition with environment variables
- Configure ALB for HTTPS (required for voice features)

### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy voice-ai-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY=your_key
```

### Azure Container Instances
```bash
# Deploy with Azure CLI
az container create \
  --resource-group myResourceGroup \
  --name voice-ai-agent \
  --image your-registry/voice-ai-agent \
  --environment-variables GROQ_API_KEY=your_key \
  --ports 8501
```

## 🔧 Performance Optimization

### For Production Deployments
1. **Enable caching**: Set `STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true`
2. **Optimize memory**: Use `--server.maxUploadSize=25` for audio files
3. **Set workers**: Use multiple Streamlit processes behind a load balancer
4. **CDN**: Serve static assets through CloudFlare or similar

### Audio Processing Optimization
```python
# In production, consider these optimizations:
# 1. Use async audio processing
# 2. Implement audio compression before upload
# 3. Cache transcription results
# 4. Use streaming STT for long audio files
```

## 🛡️ Security Considerations

### API Keys
- Never commit API keys to version control
- Use platform-specific secret management
- Rotate keys regularly

### Audio Data
- Implement audio file cleanup after processing
- Consider encryption for sensitive audio content
- Set appropriate upload limits

### HTTPS Requirements
```nginx
# Nginx configuration for voice features
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## 📊 Monitoring and Logging

### Application Metrics
- Monitor audio upload success rates
- Track transcription accuracy (in production with real STT)
- Monitor API usage and costs

### Logs
```python
# Add to your app for production logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🔄 Continuous Deployment

### GitHub Actions Example
```yaml
name: Deploy Voice AI Agent
on:
  push:
    branches: [main]
    
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        run: |
          railway deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## 📱 Mobile Considerations

The Voice AI Agent is designed to work on mobile devices:
- Responsive glass morphism UI
- Touch-optimized controls
- Mobile audio recording support
- Progressive Web App (PWA) ready

## 🆘 Troubleshooting

### Common Issues
1. **Audio upload fails**: Check file size limits and format support
2. **Recording doesn't work**: Ensure HTTPS and browser permissions
3. **Slow transcription**: Implement async processing for production
4. **Memory issues**: Set appropriate container limits for audio processing

### Debug Mode
```bash
# Run with debug information
streamlit run main.py --logger.level=debug --server.port=8501
```

## 📈 Scaling

For high-traffic deployments:
1. Use Redis for session state management
2. Implement audio processing queues (Celery/RQ)
3. Use dedicated STT services (AssemblyAI, Deepgram)
4. Consider WebSocket connections for real-time features

---

## 🎯 Platform-Specific Quick Starts

### Vercel (Not Recommended for Audio)
⚠️ Note: Vercel has limitations with audio file processing and long-running requests. Use Railway or Render instead.

### Heroku
```bash
# Deploy to Heroku
git clone https://github.com/Aniketyadav77/cold-email-generator-AI-AGENT.git
cd cold-email-generator-AI-AGENT
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

### DigitalOcean App Platform
- Connect GitHub repository
- Use Python buildpack
- Set run command: `streamlit run streamlit_app.py --server.port=$PORT`
- Add environment variables in dashboard

Choose the deployment method that best fits your needs. The Voice AI Agent is designed to work seamlessly across all major cloud platforms while maintaining its voice-first functionality.
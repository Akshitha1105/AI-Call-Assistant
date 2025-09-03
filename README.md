# 🎤 AI Voice Cloning Platform

A production-ready platform for training custom AI voices and generating speech using state-of-the-art voice cloning models.

![Platform Overview](docs/images/platform-overview.png)

## 🚀 Features

### Core Capabilities
- **Voice Training**: Upload voice samples and train custom AI voices
- **Voice Generation**: Generate speech in trained voices with emotion control
- **Multiple Models**: Support for VITS, So-VITS-SVC, and Bark models
- **Real-time Training**: Monitor training progress with live metrics
- **Voice Library**: Browse and manage trained voices

### Advanced Features
- **Multi-language Support**: Train voices in multiple languages
- **Emotion Control**: Generate speech with different emotional styles
- **Batch Processing**: Process multiple text inputs simultaneously
- **API Access**: RESTful API for integration with other applications
- **Cloud Storage**: S3/GCS integration for scalable storage

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ML Pipeline   │
│   (Streamlit)   │◄──►│   (FastAPI)     │◄──►│   (Voice       │
│                 │    │                 │    │   Training)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Auth     │    │   Database      │    │   Model        │
│   (JWT/OAuth2)  │    │   (PostgreSQL)  │    │   Storage      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance web framework
- **PostgreSQL**: Primary database
- **Redis**: Caching and job queues
- **SQLAlchemy**: Database ORM
- **JWT**: Authentication

### Frontend
- **Streamlit**: Interactive web application
- **Plotly**: Data visualization
- **Pandas**: Data manipulation

### ML Pipeline
- **PyTorch**: Deep learning framework
- **Resemblyzer**: Voice embedding extraction
- **VITS/So-VITS-SVC/Bark**: Voice cloning models
- **Librosa**: Audio processing

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Local development
- **NVIDIA GPU**: Training acceleration

## 📦 Installation

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- NVIDIA GPU (for training, optional)
- PostgreSQL 15+
- Redis 7+

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voice-cloning-platform.git
   cd voice-cloning-platform
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the platform**
   ```bash
   cd deployment/docker
   docker-compose up -d
   ```

4. **Access the platform**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Installation

1. **Install Python dependencies**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   pip install -r requirements.txt
   
   # ML Pipeline
   cd ../ml_pipeline
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb voice_cloning
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

3. **Start services**
   ```bash
   # Backend
   cd backend
   uvicorn app.main:app --reload
   
   # Frontend
   cd frontend
   streamlit run app.py
   ```

## 🎯 Usage

### 1. Voice Training

1. **Create a new voice**
   - Navigate to Voice Training
   - Enter voice details (name, description, characteristics)
   - Upload 5-10 minutes of clear audio samples

2. **Configure training**
   - Select model type (VITS, So-VITS-SVC, or Bark)
   - Adjust training parameters
   - Start training process

3. **Monitor progress**
   - View real-time training metrics
   - Track loss curves and validation scores
   - Receive completion notifications

### 2. Voice Generation

1. **Select voice**
   - Choose from your trained voices
   - Browse public voice library

2. **Input text**
   - Single text input
   - Batch text processing
   - Document upload (PDF, DOCX)

3. **Configure parameters**
   - Emotion and style control
   - Speed and pitch adjustment
   - Audio quality settings

4. **Generate and download**
   - Preview generated audio
   - Download in multiple formats
   - Save to voice library

### 3. API Usage

```python
import requests

# Authenticate
response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "email": "user@example.com",
    "password": "password"
})
token = response.json()["access_token"]

# Generate speech
headers = {"Authorization": f"Bearer {token}"}
response = requests.post("http://localhost:8000/api/v1/voices/generate", 
    headers=headers,
    json={
        "voice_id": 1,
        "text": "Hello, world!",
        "emotion": "happy",
        "speed": 1.0
    }
)

# Download audio
audio_url = response.json()["audio_url"]
```

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/voice_cloning

# Redis
REDIS_URL=redis://localhost:6379

# Storage
STORAGE_TYPE=local  # local, s3, gcs
LOCAL_STORAGE_PATH=./storage

# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=your_bucket

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Model Configuration

```yaml
model:
  type: "vits"  # vits, so-vits-svc, bark
  config:
    hidden_channels: 192
    filter_channels: 768
    filter_channels_dp: 256
    kernel_size: 3
    p_dropout: 0.1
    resblock: "1"
    resblock_kernel_sizes: [3, 7, 11]
    resblock_dilation_sizes: [[1, 3, 5], [1, 3, 5], [1, 3, 5]]
    upsample_rates: [8, 8, 2, 2]
    upsample_initial_channel: 512
    upsample_kernel_sizes: [16, 16, 4, 4]
    n_layers_q: 3
    use_spectral_norm: false
    gin_channels: 256
```

## 📊 Performance

### Training Performance
- **VITS**: 1-2 hours for 5-10 minutes of audio
- **So-VITS-SVC**: 2-4 hours for high-quality results
- **Bark**: 3-6 hours for creative voice cloning

### Generation Performance
- **Real-time**: < 1 second for short texts
- **Batch processing**: 10-50 texts per minute
- **Quality**: 8.5-9.5/10 average quality score

### Resource Requirements
- **Training**: 8GB+ RAM, NVIDIA GPU recommended
- **Inference**: 4GB+ RAM, CPU/GPU
- **Storage**: 1-5GB per trained voice

## 🚀 Deployment

### Production Deployment

1. **Cloud Platforms**
   - **AWS**: ECS, EKS, or EC2
   - **GCP**: Cloud Run, GKE, or Compute Engine
   - **Azure**: Container Instances, AKS, or VMs

2. **Kubernetes**
   ```bash
   kubectl apply -f deployment/kubernetes/
   ```

3. **Terraform**
   ```bash
   cd deployment/terraform
   terraform init
   terraform apply
   ```

### Hugging Face Spaces

1. **Create Space**
   - Choose Streamlit app
   - Upload frontend code
   - Configure environment variables

2. **Connect Backend**
   - Deploy backend to cloud platform
   - Update frontend API endpoints

## 🧪 Testing

### Run Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
pytest

# ML pipeline tests
cd ml_pipeline
pytest
```

### Test Coverage
```bash
# Generate coverage report
pytest --cov=app --cov-report=html
```

## 📈 Monitoring

### Metrics
- Training progress and loss curves
- Generation quality scores
- API response times
- Resource utilization

### Logging
- Structured logging with JSON format
- Log aggregation with ELK stack
- Error tracking and alerting

### Health Checks
- Service health endpoints
- Database connectivity
- Model availability

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Add type hints to functions
- Write comprehensive tests
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Resemblyzer**: Voice embedding extraction
- **VITS**: Fast voice cloning model
- **So-VITS-SVC**: High-quality voice conversion
- **Bark**: Creative text-to-speech
- **FastAPI**: Modern web framework
- **Streamlit**: Interactive data apps

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/voice-cloning-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/voice-cloning-platform/discussions)
- **Email**: support@voicecloning.com

## 🔮 Roadmap

### v1.1 (Q1 2024)
- [ ] Multi-speaker voice cloning
- [ ] Real-time voice conversion
- [ ] Mobile app support

### v1.2 (Q2 2024)
- [ ] Advanced emotion control
- [ ] Voice style transfer
- [ ] Batch training optimization

### v2.0 (Q3 2024)
- [ ] Zero-shot voice cloning
- [ ] Cross-language voice transfer
- [ ] Enterprise features

---

**Made with ❤️ by the Voice Cloning Team**
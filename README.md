# 🔥 Roast My Profile

**AI-powered profile picture roasting service** - Upload your profile pic and get hilariously roasted by AI vision models!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.3-blue.svg)

## ✨ Features

- 📸 **Drag-and-drop** image upload with instant preview
- 🤖 **AI Vision Analysis** using Google Gemini (or OpenAI GPT-4 Vision)
- 🎭 **Witty, Playful Roasts** that are funny, not mean
- 🛡️ **Content Moderation** to keep roasts entertaining and safe
- ⚡ **Async Processing** with job queue system
- 🎨 **Premium UI** with dark mode, glassmorphism, and smooth animations
- 🐳 **Docker Ready** for easy deployment
- ✅ **Comprehensive Tests** with pytest

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │ ───► │    Backend   │ ───► │  Gemini API │
│  React+Vite │      │    FastAPI   │      │   (Vision)  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ Worker Queue │
                    │ (Threading)  │
                    └──────────────┘
```

**Tech Stack:**
- **Backend:** FastAPI (Python), Google Gemini API
- **Frontend:** React 18, Vite
- **Styling:** Vanilla CSS with premium dark mode
- **Deployment:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Local Development

#### 1. Clone the repository

```bash
git clone <your-repo-url>
cd roast-my-profile
```

#### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

#### 3. Start the backend

```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

Backend will be running at `http://localhost:8000`

#### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be running at `http://localhost:3000`

### Docker Setup

The easiest way to run the entire stack:

```bash
# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Start all services
docker-compose up --build
```

- Frontend: `http://localhost`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## 📚 API Documentation

### Upload Image

```http
POST /api/roast
Content-Type: multipart/form-data

file: <image file>
```

**Response (202 Accepted):**
```json
{
  "job_id": "abc-123-def",
  "message": "Roast job submitted successfully",
  "status_url": "/api/roast/abc-123-def"
}
```

### Check Roast Status

```http
GET /api/roast/{job_id}
```

**Response (200 OK):**
```json
{
  "status": "completed",
  "result": {
    "roast": "Your profile pic looks like...",
    "analysis": "Image analysis details..."
  }
}
```

**Status Values:**
- `pending` - Job queued
- `processing` - AI is analyzing
- `completed` - Roast ready!
- `failed` - Something went wrong

## ⚙️ Configuration

Environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `AI_PROVIDER` | AI provider (`gemini` or `openai`) | `gemini` |
| `MAX_FILE_SIZE` | Max upload size in bytes | `10485760` (10MB) |
| `ENABLE_MODERATION` | Enable content moderation | `true` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Run Frontend Build Test

```bash
cd frontend
npm run build
```

## 🎨 Features Deep Dive

### Content Moderation

The app includes multi-layer moderation:

1. **Image Validation:** Size, dimensions, format checks
2. **Roast Content Filtering:** Blocks harmful keywords while keeping it funny
3. **Length Validation:** Ensures roasts are substantial but not essays

### AI Prompt Engineering

Two-stage prompt system:

1. **Vision Analyzer:** Detailed image analysis focusing on roastable elements
2. **Roast Generator:** Witty comedian persona with tone guidelines

See `prompts/` directory for full prompts.

### Premium UI Design

- **Dark Mode First:** Beautiful gradient backgrounds
- **Glassmorphism:** Frosted glass effects on cards
- **Micro-animations:** Hover effects, floating icons
- **Responsive:** Works on mobile and desktop

## 📁 Project Structure

```
roast-my-profile/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # App entry point
│   │   ├── routes/         # API routes
│   │   ├── services/       # AI & moderation
│   │   ├── workers/        # Queue worker
│   │   ├── utils/          # Cache utilities
│   │   └── config.py       # Configuration
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx         # Main app
│   │   └── api.js          # API client
│   ├── Dockerfile
│   └── package.json
├── prompts/                # AI prompts
├── tests/                  # Test suite
├── docker-compose.yml      # Multi-container setup
└── .github/workflows/      # CI/CD
```

## 🚢 Deployment

### Docker Production Build

```bash
docker-compose -f docker-compose.yml up -d
```

### Environment Setup

For production, ensure:
- Set `DEBUG=false`
- Use strong API keys
- Configure proper CORS origins
- Set up HTTPS/SSL
- Consider Redis for production queue (vs in-memory)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini** for amazing vision capabilities
- **FastAPI** for the excellent async web framework
- **React** for the UI library
- **Vite** for lightning-fast development

## 🔮 Future Enhancements

- [ ] Support for OpenAI GPT-4 Vision
- [ ] Redis-backed job queue for scalability
- [ ] User authentication and roast history
- [ ] Social sharing features
- [ ] Multiple roast styles (gentle, savage, professional)
- [ ] Rate limiting and abuse prevention

---

Made with 🔥 and AI • All roasts are in good fun!

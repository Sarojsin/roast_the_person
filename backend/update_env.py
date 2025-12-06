import os

content = """# Environment Configuration
# Copy this file to .env and fill in your values

# AI Provider Configuration
AI_PROVIDER=gemini  # Options: gemini, openai
GEMINI_API_KEY=AIzaSyAlprifKpxWIj8p7WeXhZzCL8d_eJYeD2c
# OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
GEMINI_MODEL=gemini-1.5-flash
# OPENAI_MODEL=gpt-4-vision-preview

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB in bytes
JOB_TIMEOUT=120  # seconds
CACHE_TTL=3600  # seconds (1 hour)

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=false

# CORS Settings (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Moderation
ENABLE_MODERATION=true
"""

with open(".env", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated .env file")

"""Configuration settings for TechXcel"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Upload Configuration
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE_MB = 10

# Analysis Configuration
MAX_ROWS_FOR_ANALYSIS = 10000
CONFIDENCE_THRESHOLD = 0.7

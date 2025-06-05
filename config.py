"""
Application configuration using environment variables.
"""
import os
from typing import Literal
from functools import lru_cache

# Load environment variables from .env file if it exists
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

# API Settings
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_BASE_PATH = os.getenv("API_BASE_PATH", "rag")

# App Settings
APP_TITLE = os.getenv("APP_TITLE", "AI Knowledge Assistant")
APP_ICON = os.getenv("APP_ICON", "🤖")
APP_LAYOUT = os.getenv("APP_LAYOUT", "wide")

# Logging Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
CONSOLE_LOGGING = os.getenv("CONSOLE_LOGGING", "true").lower() == "true"
FILE_LOGGING = os.getenv("FILE_LOGGING", "true").lower() == "true"

# Validate layout
if APP_LAYOUT not in ["wide", "centered"]:
    raise ValueError("APP_LAYOUT must be either 'wide' or 'centered'")

# API Endpoints
@lru_cache
def get_chat_endpoint() -> str:
    """Get the chat endpoint URL."""
    return f"{API_URL}/{API_BASE_PATH}/query"

@lru_cache
def get_health_endpoint() -> str:
    """Get the health check endpoint URL."""
    return f"{API_URL}/{API_BASE_PATH}/health"

# AI Knowledge Assistant Frontend

A Streamlit-based chat interface for interacting with the AI Knowledge Assistant.

## Setup

1. Make sure you have Python 3.9+ and Poetry installed
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Configure the application:
   - Copy `.env.example` to `.env`
   - Modify the values in `.env` to match your environment

## Configuration

The application can be configured using environment variables:

### API Configuration
- `API_PROTOCOL`: Protocol to use (default: "http")
- `API_HOST`: Host address of the API (default: "localhost")
- `API_PORT`: Port number of the API (default: 8000)
- `API_BASE_PATH`: Base path for the API if needed (default: "")

### Application Configuration
- `APP_TITLE`: Title of the application (default: "AI Knowledge Assistant")
- `APP_ICON`: Emoji icon for the application (default: "🤖")
- `APP_LAYOUT`: Layout mode ("wide" or "centered", default: "wide")

## Running the Application

1. Make sure the backend service is running
2. Start the Streamlit app:
   ```bash
   poetry run streamlit run app.py
   ```
3. Open your browser and navigate to http://localhost:8501

## Features

- Clean and intuitive chat interface
- Real-time communication with the backend
- Message history persistence during the session
- Responsive design that works on all devices
- Configurable endpoints and application settings
- Health checks and error handling

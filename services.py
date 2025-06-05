"""
Service layer for handling API interactions.
"""
import json
import requests
from typing import Dict, Any, Generator
from datetime import datetime

from config import get_chat_endpoint, get_health_endpoint
from logger import api_logger

class APIError(Exception):
    """Custom exception for API-related errors."""
    pass

class ChatService:
    """Service for handling chat-related API interactions."""

    @staticmethod
    def send_message(question: str, user_role: str = "admin") -> Generator[str, None, None]:
        """
        Send a message to the chat API and yield streaming responses.

        Args:
            question: The user's question
            user_role: The role of the user making the request (default: "admin")

        Yields:
            Text chunks from the response

        Raises:
            APIError: If there's an error communicating with the API
        """
        endpoint = get_chat_endpoint()

        try:
            start_time = datetime.now()

            # Make streaming request
            with requests.post(
                endpoint,
                json={"question": question, "user_role": user_role},
                stream=True,
                timeout=30
            ) as response:
                response.raise_for_status()

                # Process the streaming response
                buffer = ""
                for line in response.iter_lines():
                    if line:
                        try:
                            # Decode the line and parse JSON
                            chunk = json.loads(line.decode('utf-8'))
                            if 'content' in chunk:
                                content = chunk['content']
                                yield content

                        except json.JSONDecodeError as e:
                            api_logger.warning(f"Failed to parse chunk: {line.decode('utf-8')}")
                            continue

            # Log completion
            response_time = (datetime.now() - start_time).total_seconds()
            api_logger.info(f"Request completed in {response_time:.2f} seconds")

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to communicate with chat service: {str(e)}"
            api_logger.error(error_msg, exc_info=True)
            raise APIError(error_msg)

    @staticmethod
    def health_check() -> bool:
        """
        Check if the chat service is available.

        Returns:
            True if the service is healthy, False otherwise
        """
        endpoint = get_health_endpoint()
        api_logger.info(f"Checking health at {endpoint}")

        try:
            response = requests.get(
                endpoint,
                timeout=5
            )
            is_healthy = response.status_code == 200
            api_logger.info(f"Health check status: {'healthy' if is_healthy else 'unhealthy'}")
            return is_healthy

        except requests.exceptions.RequestException as e:
            api_logger.error(f"Health check failed: {str(e)}", exc_info=True)
            return False

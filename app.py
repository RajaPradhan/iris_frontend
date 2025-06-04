"""
Main Streamlit application.
"""
import streamlit as st
from typing import Generator

from config import APP_TITLE, APP_ICON, APP_LAYOUT
from services import ChatService, APIError
from logger import app_logger

# Configure the page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT
)

def stream_response(prompt: str) -> Generator[str, None, None]:
    """
    Create a generator for streaming the response.

    Args:
        prompt: The user's question

    Yields:
        Accumulated response text
    """
    response_text = ""
    for chunk in ChatService.send_message(prompt):
        response_text += chunk
        yield response_text
    return response_text

# Initialize session state for messages and response
if "messages" not in st.session_state:
    st.session_state.messages = []
    app_logger.info("Initialized new chat session")

# Application title
st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown("---")

# Check API health
if not ChatService.health_check():
    error_msg = "Unable to connect to the chat service. Please try again later."
    app_logger.error(error_msg)
    st.error(f"⚠️ {error_msg}")
    st.stop()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    app_logger.info(f"Received user input: {prompt}")

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        try:
            response_container = st.empty()

            # Show initial thinking message
            response_container.markdown("🤔 IRIS is thinking...")

            # Stream the response
            final_response = ""
            for response_text in stream_response(prompt):
                response_container.markdown(response_text)
                final_response = response_text

            # Store the complete response
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_response
            })
            app_logger.info("Successfully processed user request")

        except APIError as e:
            error_msg = f"Error: {str(e)}"
            app_logger.error(error_msg)
            st.error(error_msg)
            # Remove the user message if we couldn't get a response
            st.session_state.messages.pop()
            app_logger.info("Removed failed message from chat history")

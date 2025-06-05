"""
Main Streamlit application.
"""
import streamlit as st
from typing import Generator
from pathlib import Path
import base64

from config import APP_TITLE, APP_ICON, APP_LAYOUT
from services import ChatService, APIError
from logger import app_logger

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

# Configure the page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT
)

# Initialize session state for messages and response
if "messages" not in st.session_state:
    st.session_state.messages = []
    app_logger.info("Initialized new chat session")

# Initialize session state for role
if "current_role" not in st.session_state:
    st.session_state.current_role = "Operations Manager"

# Define paths
LOGO_PATH = "static/images/logo.png"
PROFILE_PIC_PATH = "static/images/profile.jpg"

# Custom CSS for logo, welcome message and sidebar
st.markdown("""
<style>
/* Full-page animated gradient background */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
body, .main {
    background: linear-gradient(-45deg, #1e1e1e, #2d2d2d, #1e1e1e, #2d2d2d);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Logo styling */
.logo-container {
    text-align: center;
    margin-top: 5vh;
    animation: fadeIn 2.5s ease forwards;
}
.logo-container img {
    margin-bottom: 1rem;
    width: 150px;
}

/* Welcome message styling */
.welcome-container {
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    animation: fadeIn 2.5s ease forwards;
}
.welcome-container h1 {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #4a4a4a, #ffffff);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
}
.welcome-container p {
    color: #ddd;
    font-size: 1.2rem;
    margin-top: 0.5rem;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a1a, #2d2d2d);
    padding: 2rem 1rem;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
.sidebar-content {
    text-align: center;
}
.profile-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 2rem;
    margin-bottom: 2rem;
}
.profile-image {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 1.5rem;
    border: 4px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}
.profile-name {
    font-size: 1.4rem;
    font-weight: 600;
    margin: 0.5rem 0 0.2rem;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.profile-role {
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    font-size: 1rem;
}
.sidebar-divider {
    margin: 2rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    width: 100%;
}

/* Role selector styling */
div[data-testid="stSelectbox"] {
    margin-top: 1rem;
}
div[data-testid="stSelectbox"] > div {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stSelectbox"] > div:hover {
    border-color: rgba(255, 255, 255, 0.2) !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}
div[data-testid="stSelectbox"] > div > div {
    color: rgba(255, 255, 255, 0.9) !important;
}

/* Role heading style */
.role-heading {
    color: rgba(255, 255, 255, 0.7);
    font-size: 1.1rem;
    font-weight: 500;
    margin: 0.5rem 0 0.2rem;
}

/* Hide Streamlit branding in sidebar */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Streamlit warning message styling */
.stAlert {
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Fade-in animation */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Blinking dots animation */
@keyframes blink {
    0% { opacity: 0.2; }
    20% { opacity: 1; }
    100% { opacity: 0.2; }
}

.thinking-dots span {
    animation: blink 1.4s infinite;
    display: inline-block;
    margin: 0 1px;
}

.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
</style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    # Profile section
    if Path(PROFILE_PIC_PATH).exists():
        st.markdown(
            f"""
            <div class="profile-section">
                <img src="data:image/jpeg;base64,{base64.b64encode(open(PROFILE_PIC_PATH, "rb").read()).decode()}" class="profile-image" />
                <h4 class="profile-name">Joshua Lieb</h4>
                <p class="profile-role">{st.session_state.current_role}</p>
            </div>
            <hr class="sidebar-divider" />
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Profile picture not found. Using default settings.")

    # Role selector
    st.markdown(
        """
        <div style='text-align: center;'>
            <h4 class="role-heading">Role</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Update the current role when selection changes
    new_role = st.selectbox(
        "Please select your Role",
        ["Operations Manager", "HR Manager", "Finance Manager", "Marketing Manager", "Product Manager", "IT Director"],
        label_visibility="collapsed",
        key="role_selector"
    )

    if new_role != st.session_state.current_role:
        st.session_state.current_role = new_role
        st.rerun()  # Rerun the app to update the displayed role

# Main content
# Display logo and welcome message
if Path(LOGO_PATH).exists():
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{base64.b64encode(open(LOGO_PATH, "rb").read()).decode()}" /></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="welcome-container">
            <h1>Welcome to IRIS</h1>
            <p>Your Intelligent Response & Information System<br><i>"Empowering clarity through conversation."</i></p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("Logo file not found!")

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

            # Show initial thinking message with blinking dots
            response_container.markdown('🤔 IRIS is thinking<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span>', unsafe_allow_html=True)

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

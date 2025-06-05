"""
Main Streamlit application.
"""
import streamlit as st
from typing import Generator, Dict, Set
from pathlib import Path
import base64
from dataclasses import dataclass

from config import APP_TITLE, APP_ICON, APP_LAYOUT
from services import ChatService, APIError
from logger import app_logger

@dataclass
class Department:
    name: str
    drive_folders: list[str]
    allowed_roles: set[str]

# Department configurations
DEPARTMENTS: Dict[str, Department] = {
    "hr": Department(
        name="hr",
        drive_folders=["HR Documents", "HR Policies", "Employee Records"],
        allowed_roles={"admin", "hr_manager", "hr_staff"}
    ),
    "engineering": Department(
        name="engineering",
        drive_folders=["Engineering", "Technical Docs", "Architecture"],
        allowed_roles={"admin", "tech_lead", "engineer"}
    ),
    "sales": Department(
        name="sales",
        drive_folders=["Sales", "Customer Data", "Contracts"],
        allowed_roles={"admin", "sales_manager", "sales_rep"}
    ),
    "finance": Department(
        name="finance",
        drive_folders=["Finance", "Accounting", "Budget"],
        allowed_roles={"admin", "finance_manager", "accountant"}
    ),
    "operations": Department(
        name="operations",
        drive_folders=["Operations", "SOPs", "Processes", "Workflows"],
        allowed_roles={"admin", "ops_manager", "ops_staff", "process_analyst"}
    ),
    "general": Department(
        name="general",
        drive_folders=["Public", "Company Policies", "General"],
        allowed_roles={
            "admin", "hr_manager", "tech_lead", "sales_manager",
            "finance_manager", "ops_manager", "hr_staff", "engineer",
            "sales_rep", "accountant", "ops_staff", "process_analyst"
        }
    )
}

# Get all unique roles
ALL_ROLES: Set[str] = {role for dept in DEPARTMENTS.values() for role in dept.allowed_roles}

# Role display names (for better UI presentation)
ROLE_DISPLAY_NAMES = {
    "admin": "Administrator",
    "hr_manager": "HR Manager",
    "hr_staff": "HR Staff",
    "tech_lead": "Technical Lead",
    "engineer": "Software Engineer",
    "sales_manager": "Sales Manager",
    "sales_rep": "Sales Representative",
    "finance_manager": "Finance Manager",
    "accountant": "Accountant",
    "ops_manager": "Operations Manager",
    "ops_staff": "Operations Staff",
    "process_analyst": "Process Analyst"
}

def get_department_for_role(role: str) -> str:
    """Get the primary department for a role."""
    for dept_name, dept in DEPARTMENTS.items():
        if role in dept.allowed_roles and dept_name != "general":
            return dept_name
    return "general"

def stream_response(prompt: str, user_role: str) -> Generator[str, None, None]:
    """
    Create a generator for streaming the response.

    Args:
        prompt: The user's question
        user_role: The role of the user making the request

    Yields:
        Accumulated response text
    """
    response_text = ""
    for chunk in ChatService.send_message(prompt, user_role=user_role):
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
    st.session_state.current_role = "admin"  # Default role

def on_role_change():
    """Handle role change events."""
    app_logger.info(f"Role changed to: {st.session_state.role_selector}")
    st.session_state.current_role = st.session_state.role_selector
    # Clear messages when role changes to maintain context separation
    st.session_state.messages = []

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

/* Role selector group styling */
.role-group {
    margin-top: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
    background-color: rgba(255, 255, 255, 0.05);
}
.role-group-title {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Department indicator */
.department-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    background-color: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
    margin-top: 0.5rem;
}
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
                <p class="profile-role">{ROLE_DISPLAY_NAMES.get(st.session_state.current_role, st.session_state.current_role)}</p>
                <div class="department-tag">{get_department_for_role(st.session_state.current_role).title()} Department</div>
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
            <h4 class="role-heading">Select Role</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Update the current role when selection changes
    st.selectbox(
        "Please select your Role",
        sorted(ALL_ROLES),
        format_func=lambda x: ROLE_DISPLAY_NAMES.get(x, x),
        key="role_selector",
        label_visibility="collapsed",
        on_change=on_role_change,
        index=sorted(ALL_ROLES).index(st.session_state.current_role)
    )

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
    app_logger.info(f"Current role: {st.session_state.current_role}")  # Add logging for debugging

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

            # Stream the response with user role
            final_response = ""
            current_role = st.session_state.current_role  # Capture current role
            app_logger.info(f"Sending request with role: {current_role}")  # Add logging for debugging

            for response_text in stream_response(prompt, user_role=current_role):
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

import streamlit as st
import time
import base64
# import requests

# ---- Page Configuration ----
st.set_page_config(page_title="IRIS", layout="centered")

# ---- Session State Initialization ----
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---- Helper: Load an image and convert to Base64 for inline HTML ----
def get_image_base64(image_path):
    """
    Read a local image file (e.g., 'static/logo_home.png') and return
    a data URI string like 'data:image/png;base64,...' so we can embed it
    directly in HTML.
    """
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

# Convert images to base64
img_profile_base64 = get_image_base64("static/profile.jpg")      # sidebar avatar
img_sidebar_logo_base64 = get_image_base64("static/logo.png")    # sidebar logo
img_home_logo_base64 = get_image_base64("static/logo_home.png")  # welcome-screen logo

# # ---- Read API Key (assumed stored in st.secrets) ----
# API_KEY = st.secrets["api"]["key"]

# ---- Sidebar Content ----
with st.sidebar:
    # Sidebar logo (embedded via Base64)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{img_sidebar_logo_base64}" style="width:50%;" />
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Profile section: avatar, name, and company
    st.markdown(f"""
        <div style='text-align: center; margin-top: 1.5rem;'>
            <img src="{img_profile_base64}" style="border-radius: 50%; width: 100px; height: 100px; object-fit: cover;" />
            <h4 style='margin: 0.5rem 0 0.2rem;'>Max Mustermann</h4>
            <p style='color: gray; margin: 0;'>IRIS Ltd.</p>
        </div>
        <hr style='margin: 1.5rem 0;' />
    """, unsafe_allow_html=True)

    # Role selector header
    st.markdown("""
        <div style='text-align: center; margin-top: 1.5rem;'>
            <h4 style='margin: 0.5rem 0 0.2rem;'>Role</h4>
        </div>
    """, unsafe_allow_html=True)

    # Selectbox for choosing a role
    role = st.selectbox(
        "Please select your Role",
        ["Operations Manager", "HR Manager", "Finance Manager", "Marketing Manager", "Product Manager", "IT Director"]
    )

    # Change button (UI only)
    st.button("Change")

    # Settings header
    st.markdown("<h4 style='text-align: center;'>Settings</h4>", unsafe_allow_html=True)

    # custom buttons under "Settings"
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem;">
        <button style='width: 200px; padding: 0.5rem 1rem; border-radius: 6px; border: none; background-color: #2F61F6; color: white; font-weight: 600; cursor: pointer;'>My Profile</button>
        <button style='width: 200px; padding: 0.5rem 1rem; border-radius: 6px; border: none; background-color: #2F61F6; color: white; font-weight: 600; cursor: pointer;'>Language & Time Zone</button>
        <button style='width: 200px; padding: 0.5rem 1rem; border-radius: 6px; border: none; background-color: #2F61F6; color: white; font-weight: 600; cursor: pointer;'>Notifications & Alerts</button>
        <button style='width: 200px; padding: 0.5rem 1rem; border-radius: 6px; border: none; background-color: #2F61F6; color: white; font-weight: 600; cursor: pointer;'>Security & Privacy</button>
        <button style='width: 200px; padding: 0.5rem 1rem; border-radius: 6px; border: none; background-color: #2F61F6; color: white; font-weight: 600; cursor: pointer;'>Appearance & Preferences</button>
        <button style='width: 200px; padding: 0.5rem 1rem; border-radius: 6px; border: none; background-color: #2F61F6; color: white; font-weight: 600; cursor: pointer;'>Admin & Organization Settings</button>
        <button style='width: 200px; padding: 0.5rem 1rem; border-radius: 6px; border: none; background-color: #2F61F6; color: white; font-weight: 600; cursor: pointer;'>Help & Support</button>
    </div>
    """, unsafe_allow_html=True)

    # Feedback text area (UI only; no backend logic)
    st.text_area("Feedback", placeholder="Write your feedback here...")

    # Support button (UI only)
    st.button("Support")


# ---- Global Styles & Animations ----
# This block handles:
#  - Sidebar button hover/normal states (no glow)
#  - Full-page gradient background animation
#  - Intro fade-in effect
#  - Chat-input button styling (kept simple, no heavy glow)
st.markdown(
    """
    <style>
    /* Sidebar buttons: keep solid color, no glow or box-shadow */
    section[data-testid="stSidebar"] button {
        background-color: #2F61F6 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        transition: background-color 0.2s ease;
        cursor: pointer;
        box-shadow: none !important;  /* remove any default glow */
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: #244EDB !important;
        /* no glowing box-shadow on hover */
    }

    /* Full-page animated gradient background */
    @keyframes gradientBG {
      0% {background-position: 0% 50%;}
      50% {background-position: 100% 50%;}
      100% {background-position: 0% 50%;}
    }
    body, .main {
      background: linear-gradient(-45deg, #1e3c72, #2a5298, #4b6cb7, #182848);
      background-size: 400% 400%;
      animation: gradientBG 15s ease infinite;
      color: white;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Remove glow animation from Welcome heading */
    /* (Previously .welcome h1 had a textGlow effect; it is now plain) */
    .welcome h1 {
      font-size: 3.5rem;
      font-weight: 900;
      background: linear-gradient(90deg, #2F61F6, #244EDB);
      background-clip: text;
      -webkit-background-clip: text;
      color: transparent;
      /* no textGlow animation */
    }

    /* Intro paragraph fade-in (kept for subtle effect) */
    .intro {
      animation: fadeIn 2.5s ease forwards;
      opacity: 0;
      font-size: 1.2rem;
      max-width: 600px;
      margin-top: 20px;
      line-height: 1.5;
      color: #ddd;
    }
    @keyframes fadeIn {
      to { opacity: 1; }
    }

    /* Chat input button styling: simple gradient, no heavy glow */
    div.stButton > button {
      background: linear-gradient(90deg, #2F61F6, #244EDB);
      color: white;
      border-radius: 50px;
      padding: 12px 36px;
      font-weight: 700;
      font-size: 1.2rem;
      /* reduced box-shadow for minimal effect */
      box-shadow: 0 0 5px rgba(47, 97, 246, 0.5);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      cursor: pointer;
      margin-top: 40px;
    }
    div.stButton > button:hover {
      transform: scale(1.05);
      /* no strong glow on hover */
      box-shadow: 0 0 10px rgba(36, 78, 219, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Welcome Screen & Chat Simulation ----
if not st.session_state.show_chat:
    # Display the base64-encoded logo_home.png above "Welcome to IRIS!"
    st.markdown(
        f"""
        <div style="text-align:center; margin-top: 5vh;">
            <img src="{img_home_logo_base64}" width="150" style="margin-bottom: 1rem;" />
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Welcome header (centered on page) — now without glow animation
    st.markdown(
        """
        <div style="text-align:center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;" class="welcome">
            <h1>Welcome to IRIS!</h1>
            <p>Your Intelligent Response & Information System<br><i>“Empowering clarity through conversation.”</i></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Additional CSS for chat bubbles and typing indicator
    st.markdown(
        """
        <style>
        /* Message bubble container */
        .message {
            padding: 0.9em 1.3em;
            border-radius: 1.2em;
            margin: 0.75em 0;
            max-width: 80%;
            word-wrap: break-word;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            font-size: 1.05rem;
            transition: all 0.3s ease;
            font-family: "Segoe UI", sans-serif;
            line-height: 1.6;
        }
        /* User message style */
        .user-msg {
            background: linear-gradient(145deg, #0b93f6, #2F61F6);
            margin-left: auto;
            text-align: right;
            color: white;
        }
        /* Bot message style */
        .bot-msg {
            background: linear-gradient(145deg, #ffffff, #e5ecff);
            margin-right: auto;
            text-align: left;
            color: #111;
            border-left: 4px solid #2F61F6;
        }
        /* Typing indicator animation */
        .typing {
            font-style: italic;
            opacity: 0.6;
            margin-top: -10px;
            animation: blink 1s linear infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 0.4; }
            50% { opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Render any existing chat history from session_state
    for role, msg in st.session_state.chat:
        css_class = "user-msg" if role == "user" else "bot-msg"
        st.markdown(f"<div class='message {css_class}'>{msg}</div>", unsafe_allow_html=True)

    # Chat input widget
    user_input = st.chat_input("How can I help you today?")

    if user_input:
        # Append user message to session_state
        st.session_state.chat.append(("user", user_input))
        # Display the user's message bubble immediately
        st.markdown(f"<div class='message user-msg'>{user_input}</div>", unsafe_allow_html=True)

        # Prepare a container for the bot response (with typing effect)
        response_container = st.empty()
        full_response = ""
        fake_response = (
            f"Sure! Here's IRIS's answer to: **{user_input}**  \n\n"
            "This is a placeholder, but the typing effect is much smoother now!"
        )

        # Show "IRIS is thinking..." first
        with response_container:
            st.markdown(
                "<div class='message bot-msg'><span class='typing'>IRIS is thinking...</span></div>",
                unsafe_allow_html=True,
            )
        time.sleep(1.0)

        # Simulate streaming word by word
        for word in fake_response.split():
            full_response += word + " "
            response_container.markdown(
                f"<div class='message bot-msg'>{full_response.strip()}</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.04)

        # Finally, store the complete bot response
        st.session_state.chat.append(("bot", full_response.strip()))

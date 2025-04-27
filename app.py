import streamlit as st
from chatbot import ask_gemini
import datetime
import time
import re

# --- Streamlit Config ---
st.set_page_config(page_title="Asha AI - Career Guide", page_icon="asa.png", layout="wide")

# --- Session State Init ---
for key, default in {
    "page": "login",
    "logged_in": False,
    "email": None,
    "profile_picture": None,
    "chat_history": [],
    "chat_dates": [],
    "name": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Themes ---
light_theme = """
<style>
body, .stApp { background-color: #FAF9F6; color: black; font-style: italic; }
section[data-testid="stSidebar"] { background-color: #FAF9F6; }
.chat-container { display: flex; flex-direction: column; }
.chat-bubble { max-width: 60%; padding: 12px 20px; margin: 8px; border-radius: 20px; font-size: 17px; }
.user-bubble { background-color: #DCF8C6; align-self: flex-end; }
.bot-bubble { background-color: #F1F0F0; align-self: flex-start; }
.typing { font-style: italic; color: black; }
</style>
"""

dark_theme = """
<style>
body, .stApp { background-color: #1E1E1E; color: white; }
section[data-testid="stSidebar"] { background-color: #292929; }
.chat-container { display: flex; flex-direction: column; }
.chat-bubble { max-width: 60%; padding: 12px 20px; margin: 8px; border-radius: 20px; font-size: 17px; }
.user-bubble { background-color: #4CAF50; color: white; align-self: flex-end; }
.bot-bubble { background-color: #333333; color: white; align-self: flex-start; }
.typing { font-style: italic; color: lightgray; }
</style>
"""



def login_page():
    st.markdown("<h1 style='text-align: center;'>🌸 Welcome to Asha AI 🌸</h1>", unsafe_allow_html=True)
    try:
        st.image("asa.png", width=150)
    except Exception:
        st.image("asa.png", width=150)

    st.markdown("<h3 style='text-align: center;'>Your Career Growth Assistant</h3>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("🔵 Continue with Google", use_container_width=True)
        email = st.text_input("📧 Enter your Email Address:", placeholder="example@gmail.com")
        st.session_state.name = st.text_input("👤 Enter your Name:", value=st.session_state.name)

        if st.button("Login", use_container_width=True):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                st.session_state.logged_in = True
                st.session_state.email = email
                st.session_state.page = "chat"
                st.success(f"Welcome, {st.session_state.name or 'Guest'}!")
                st.rerun()
            else:
                st.error("Please enter a valid email address.")

    st.markdown("---")
    st.caption("We care about your privacy and security. 🔒")


def chat_page():
    with st.sidebar:
        if st.session_state.profile_picture:
            st.image(st.session_state.profile_picture, width=100)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=100)

        st.title("⚙️ Settings")
        theme_mode = st.radio("Choose Theme Mode:", ("Light Mode", "Dark Mode"), index=1)

        if st.button("🧹 Clear Chat"):
            st.session_state.chat_history.clear()
            st.session_state.chat_dates.clear()
            st.success("Chat history cleared!")

        if st.button("🚪 Logout"):
            for key in ["page", "logged_in", "email", "profile_picture", "chat_history", "chat_dates", "name"]:
                st.session_state.pop(key, None)
            st.rerun()

        st.markdown("---")
        st.subheader("💬 Previous Chats")
        if not st.session_state.chat_history:
            st.caption("No previous chats yet.")
        else:
            for idx, (sender, message) in enumerate(st.session_state.chat_history):
                chat_time = st.session_state.chat_dates[idx] if idx < len(st.session_state.chat_dates) else "Unknown"
                st.markdown(f"- 🧑‍💼 **[{chat_time}]** {message[:30]}...")

    st.markdown(light_theme if theme_mode == "Light Mode" else dark_theme, unsafe_allow_html=True)

    st.title(f"💬 Asha AI Chatbot - Hello {st.session_state.name or 'Guest'}!")
    chat_placeholder = st.container()

    with chat_placeholder:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for sender, message in st.session_state.chat_history:
            bubble_class = 'user-bubble' if sender == 'user' else 'bot-bubble'
            emoji = '🧑‍💼' if sender == 'user' else '🧑‍💻'
            st.markdown(f"<div class='chat-bubble {bubble_class}'>{emoji} {message}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Type your career-related question...")

    if user_input:
        timestamp = datetime.datetime.now().strftime("%d-%b %H:%M")
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_dates.append(timestamp)

        with st.spinner('🤖 Asha AI is typing...'):
            response = ask_gemini(user_input)

        st.session_state.chat_history.append(("bot", response))
        st.session_state.chat_dates.append(timestamp)

        st.rerun()


# --- Main Controller ---
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "chat":
    chat_page()

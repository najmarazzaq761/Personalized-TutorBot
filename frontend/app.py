# frontend/app.py
import streamlit as st
import asyncpg  # type: ignore
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

st.set_page_config(page_title="Personalized TutorBot", layout="centered")

# 🌈 Custom CSS
st.markdown("""
    <style>
        body { background-color: #f9f9fb; }
        .title { font-size:40px; color:#4A4A8C; font-weight:600; text-align:center; }
        .sub { font-size:20px; color:#888; text-align:center; margin-bottom:20px; }
        .stTextInput>div>div>input {
            border: 1px solid #ccc; border-radius: 10px; padding: 10px;
        }
        .stButton>button {
            background-color: #4A4A8C; color: white; font-size: 16px;
            padding: 10px 20px; border-radius: 8px; margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# UI Title
st.markdown('<div class="title">🤖 TutorBot Login/Register</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Your AI-powered learning assistant</div>', unsafe_allow_html=True)

# Form type toggle
form_type = st.radio("Select action:", ["Login", "Register"])

# Inputs
name = st.text_input("Name (required for registration)", "") if form_type == "Register" else ""
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# DB Functions
async def register_user(name, email, password):
    conn = await asyncpg.connect(DB_URL)
    try:
        await conn.execute("INSERT INTO users (name, email, password) VALUES ($1, $2, $3)", name, email, password)
        return True
    except asyncpg.exceptions.UniqueViolationError:
        return False
    finally:
        await conn.close()

async def login_user(email, password):
    conn = await asyncpg.connect(DB_URL)
    user = await conn.fetchrow("SELECT * FROM users WHERE email=$1 AND password=$2", email, password)
    await conn.close()
    return user

# Button handling
if st.button(form_type):
    if form_type == "Register":
        if not name or not email or not password:
            st.warning("⚠️ Please fill all fields.")
        else:
            result = asyncio.run(register_user(name, email, password))
            if result:
                st.success("✅ Registered successfully! Now please log in.")
            else:
                st.error("❌ Email already exists.")
    else:
        if not email or not password:
            st.warning("⚠️ Enter email and password.")
        else:
            user = asyncio.run(login_user(email, password))
            if user:
                st.success(f"✅ Welcome, {user['name']}!")
                st.session_state.user = dict(user)
                st.session_state.user_name = user['name']
                st.switch_page("pages/chatbot.py")  # correct relative path from /frontend
            else:
                st.error("❌ Invalid email or password.")

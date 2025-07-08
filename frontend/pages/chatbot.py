# # frontend/pages/chatbot.py
# import streamlit as st
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()
# API_URL = os.getenv("API_URL", "http://localhost:8000/tutor")

# st.set_page_config(page_title="TutorBot Chat", layout="wide")

# # 🌈 Custom styling
# st.markdown("""
# <style>
#     .title { font-size: 36px; font-weight: bold; color: #4A4A8C; text-align: center; margin-top: 10px; }
#     .chat-box {
#         background-color: #f5f7ff;
#         padding: 15px;
#         border-radius: 12px;
#         margin: 10px 0;
#     }
#     .stTextInput>div>div>input {
#         border: 1px solid #ccc;
#         padding: 10px;
#         border-radius: 8px;
#     }
#     .stChatInputContainer {
#         background-color: #ffffff;
#         padding: 10px 20px;
#         border-radius: 10px;
#         box-shadow: 0 1px 4px rgba(0,0,0,0.1);
#     }
# </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="title">💬 TutorBot — Learn AI & Coding</div>', unsafe_allow_html=True)

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "user" not in st.session_state:
#     st.warning("🔐 Please login first.")
#     st.stop()

# user_name = st.session_state.user["name"]
# st.success(f"👋 Hello, {user_name}! Let's start learning.")

# # Display chat history
# for msg in st.session_state.chat_history:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Chat input
# prompt = st.chat_input("🎯 What do you want to learn?")
# code_input = st.text_area("📝 Optional: Paste your code for review", height=150)

# if prompt:
#     st.session_state.chat_history.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
#         if code_input:
#             st.markdown(f"🧾 Submitted code:\n```python\n{code_input}\n```")

#     with st.spinner("🧠 TutorBot is generating your personalized content..."):
#         try:
#             payload = {
#                 "query": prompt,
#                 "user_id": st.session_state.user["id"],
#                 "code": code_input if code_input else None
#             }

#             res = requests.post(API_URL, json=payload)

#             if res.ok:
#                 data = res.json()
#                 output = data.get("reply", "No response received.")
#                 st.session_state.chat_history.append({"role": "assistant", "content": output})
#                 with st.chat_message("assistant"):
#                     st.markdown(output)
#             else:
#                 st.error(f"❌ Backend returned error {res.status_code}")
#                 st.session_state.chat_history.append({
#                     "role": "assistant", 
#                     "content": "❌ Something went wrong. Please try again."
#                 })
#         except Exception as e:
#             st.error(f"⚠️ Exception: {e}")
#             st.session_state.chat_history.append({
#                 "role": "assistant", 
#                 "content": f"⚠️ Unexpected error: {e}"
#             })


import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/tutor")

st.set_page_config(page_title="TutorBot Chat", layout="wide")

st.markdown("""
<style>
    .title { font-size: 36px; font-weight: bold; color: #4A4A8C; text-align: center; margin-top: 10px; }
    .stTextInput>div>div>input, .stTextArea textarea {
        border: 1px solid #ccc; padding: 10px; border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💬 TutorBot — Learn AI & Coding</div>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user" not in st.session_state:
    st.warning("🔐 Please login first.")
    st.stop()

user_name = st.session_state.user["name"]
st.success(f"👋 Hello, {user_name}! Let's start learning.")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("🎯 What do you want to learn?")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("🧠 TutorBot is generating your personalized content..."):
        try:
            payload = {
                "query": prompt,
                "user_id": st.session_state.user["id"],
                "code": None  # no code initially
            }

            res = requests.post(API_URL, json=payload)

            if res.ok:
                data = res.json()
                output = data.get("reply", "No response received.")
                st.session_state.chat_history.append({"role": "assistant", "content": output})
                with st.chat_message("assistant"):
                    st.markdown(output)

                # ✅ Show code box after exercise
                st.markdown("---")
                st.subheader("📝 Submit your solution to the coding challenge above:")

                code_input = st.text_area("Paste your code here:", height=200)

                if st.button("🧠 Review My Code"):
                    review_payload = {
                        "topic": prompt,
                        "code": code_input
                    }
                    review_res = requests.post(f"{API_URL}/review", json=review_payload)
                    if review_res.ok:
                        review_out = review_res.json().get("review", "No feedback received.")
                        st.session_state.chat_history.append({"role": "assistant", "content": review_out})
                        with st.chat_message("assistant"):
                            st.markdown(review_out)
                    else:
                        st.error("❌ Failed to get code review.")
            else:
                st.error(f"❌ Backend returned error {res.status_code}")
        except Exception as e:
            st.error(f"⚠️ Exception: {e}")

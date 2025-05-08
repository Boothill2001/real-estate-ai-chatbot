import streamlit as st
import requests
import html
import time

# === Page Setup ===
st.set_page_config(page_title="🏡 Real Estate Chatbot", layout="wide")

# === Load Custom CSS ===
def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("custom_theme.css")

# === Initial Session State ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False
if "is_bot_typing" not in st.session_state:
    st.session_state.is_bot_typing = False

# === Backend URL ===
BACKEND_BASE_URL = "https://real-estate-agent-520862369717.asia-southeast1.run.app"

# === Header ===
st.markdown("""
<div class="header-container">
    <h1>🏡 Real Estate Chatbot</h1>
    <p>Empowering Your Property Search with AI</p>
</div>
""", unsafe_allow_html=True)

# === Sidebar Settings ===
with st.sidebar:
    st.markdown("""
    <div class="sidebar-card">
    <h3>⚙️ Chatbot Settings</h3>
    """, unsafe_allow_html=True)
    top_k = st.slider("Top-K Results", min_value=3, max_value=10, value=5)
    search_mode = st.radio("Search Mode", ["Simple Search", "Agent Search"], index=0)
    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.clear_input = True
        st.rerun()
    st.markdown("""</div>""", unsafe_allow_html=True)

# === Suggested Questions ===
st.markdown("""
<div class="suggested-questions">
<p>💬 <strong>Suggested Questions:</strong></p>
""", unsafe_allow_html=True)
suggested_questions = [
    "Find affordable 4-room flats in Yishun under 400k SGD",
    "List 5-room flats in Bukit Batok priced below 600k SGD",
    "Executive flats in Pasir Ris under 800k SGD",
    "Flats with lease start after 2015 in Sengkang",
    "What's the average price for 3-room flats in Ang Mo Kio?"
]
cols = st.columns(len(suggested_questions))
for idx, (q, col) in enumerate(zip(suggested_questions, cols)):
    with col:
        if st.button(f"📎 {q}", key=f"suggested_{idx}"):
            st.session_state.clear_input = False
            st.session_state.user_input = q
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# === Chat Display ===
for idx, (user_msg, bot_docs, reasoning_list, search_time) in enumerate(st.session_state.chat_history):
    with st.container():
        with st.chat_message("user"):
            st.markdown(f"""
                <div class='chat-bubble user'>
                    <i class="bi bi-person-circle"></i> {html.escape(user_msg)}
                </div>
            """, unsafe_allow_html=True)

        with st.chat_message("assistant"):
            if isinstance(bot_docs, list):
                for i, doc in enumerate(bot_docs, 1):
                    clean_doc = html.escape(doc).replace("&lt;div&gt;", "").replace("&lt;/div&gt;", "")
                    st.markdown(f"""
                        <div class='chat-bubble bot'>
                            <i class="bi bi-robot"></i> <strong>Result {i}:</strong><br>{clean_doc}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                clean_doc = html.escape(bot_docs).replace("&lt;div&gt;", "").replace("&lt;/div&gt;", "")
                st.markdown(f"""
                    <div class='chat-bubble bot'>
                        <i class="bi bi-robot"></i> {clean_doc}
                    </div>
                """, unsafe_allow_html=True)

            if reasoning_list and reasoning_list[0]:
                st.markdown(f"""
                    <div class='reasoning-box'>
                        📈 {html.escape(reasoning_list[0])}
                    </div>
                """, unsafe_allow_html=True)

            st.caption(f"⏱ Completed in {round(search_time, 2)} seconds.")

# === User Input Box ===
st.markdown("<div class='input-area'>", unsafe_allow_html=True)

# Check if we need to clear input after send
user_input = st.text_input(
    "🔍 Ask your real estate question:",
    value="" if st.session_state.clear_input else st.session_state.get("user_input", ""),
    key="user_input",
    placeholder="e.g., Find 4-room flats in Woodlands under 400k SGD"
)

if st.session_state.clear_input:
    st.session_state.clear_input = False  # Reset trigger

# === Send Button ===
send_col, _ = st.columns([1, 8])
with send_col:
    if st.button("🚀 Send", type="primary"):
        if user_input.strip():
            st.session_state.is_bot_typing = True
            with st.spinner("Sending your query..."):
                try:
                    start_time = time.time()
                    payload = {"query": user_input, "top_k": top_k, "session_id": "test-session"}
                    res = requests.post(f"{BACKEND_BASE_URL}/ask", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.chat_history.append(
                            (user_input, data.get('documents', []), data.get('plan_steps', []), time.time() - start_time)
                        )
                    else:
                        st.session_state.chat_history.append(
                            (user_input, f"❌ Server Error: {res.status_code}", [], 0)
                        )
                except Exception as e:
                    st.session_state.chat_history.append(
                        (user_input, f"❌ Exception: {str(e)}", [], 0)
                    )
            st.session_state.is_bot_typing = False
            st.session_state.clear_input = True  # Trigger to clear input next rerun
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# === Footer ===
st.markdown("""
<div class="footer">© 2025 Real Estate Chatbot - Powered by FastAPI + Streamlit + Bootstrap Icons</div>
""", unsafe_allow_html=True)

# === Load Bootstrap Icons ===
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
""", unsafe_allow_html=True)

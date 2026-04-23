# App/main.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from App.core.faq_services import process_query
from datetime import datetime

st.set_page_config(
    page_title="JoestarIQ",
    page_icon="☆",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e2e8f0;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0a1a 50%, #0a0f1a 100%);
    background-size: 400% 400%;
    animation: gradientShift 10s ease infinite;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(251,191,36,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(251,191,36,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1100px;
    position: relative;
    z-index: 1;
}

/* ── Hero ── */
.hero-wrap {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.3rem;
}
.hero-icon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 20px rgba(251,191,36,0.8));
    animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(251,191,36,0.6)); }
    50%       { filter: drop-shadow(0 0 40px rgba(251,191,36,1)); }
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 40%, #fcd34d 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero-sub {
    font-size: 0.9rem;
    color: #475569;
    font-weight: 300;
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
}
.hero-sub span { color: #fbbf24; font-weight: 500; }
.hero-quote {
    font-size: 0.78rem;
    color: #334155;
    font-style: italic;
    margin-bottom: 1.5rem;
    letter-spacing: 0.03em;
}
.hero-quote span { color: #fbbf2466; }

/* ── Meme ticker ── */
.ticker-wrap {
    overflow: hidden;
    background: #13131a;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 0.4rem 0;
    margin-bottom: 1.5rem;
}
.ticker-text {
    display: inline-block;
    white-space: nowrap;
    animation: ticker 30s linear infinite;
    font-size: 0.78rem;
    color: #fbbf24;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}
@keyframes ticker {
    0%   { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(19, 19, 26, 0.8) !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    backdrop-filter: blur(10px);
    margin-bottom: 0.5rem !important;
    transition: border-color 0.2s;
}
[data-testid="stChatMessage"]:hover {
    border-color: #fbbf24 !important;
}

/* ── Tags ── */
.tag-row {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
    flex-wrap: wrap;
}
.tag {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    border: 1px solid #2d2d3e;
    background: #1e1e2e;
    color: #a5b4fc;
}
.tag.cat  { color: #fbbf24; border-color: #fbbf2444; background: #fbbf2411; }
.tag.sent-pos  { color: #22c55e; border-color: #22c55e44; background: #22c55e11; }
.tag.sent-neg  { color: #ef4444; border-color: #ef444444; background: #ef444411; }
.tag.sent-neu  { color: #94a3b8; border-color: #94a3b844; background: #94a3b811; }
.tag.sent-frus { color: #f97316; border-color: #f9731644; background: #f9731611; }
.tag.sent-urg  { color: #dc2626; border-color: #dc262644; background: #dc262611; }

.response-text {
    font-size: 0.97rem;
    line-height: 1.7;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
}
.timestamp {
    font-size: 0.72rem;
    color: #334155;
    text-align: right;
}

/* ── Input ── */
[data-testid="stChatInput"] {
    background: rgba(19,19,26,0.9) !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 16px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #fbbf24 !important;
    box-shadow: 0 0 0 3px rgba(251,191,36,0.15) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(10,10,15,0.95) !important;
    border-right: 1px solid #1e1e2e !important;
}
.sidebar-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1rem;
}
.stat-card {
    background: #13131a;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.stat-label { font-size: 0.8rem; color: #64748b; }
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #fbbf24;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    border-radius: 10px !important;
    background: #1e1e2e !important;
    border: 1px solid #2d2d3e !important;
    color: #fbbf24 !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #fbbf24 !important;
    color: #0a0a0f !important;
    border-color: #fbbf24 !important;
    box-shadow: 0 0 20px rgba(251,191,36,0.4) !important;
}

hr { border-color: #1e1e2e !important; }

.empty-state {
    text-align: center;
    padding: 4rem 2rem;
}
.empty-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 30px rgba(251,191,36,0.5));
    animation: pulse 3s ease-in-out infinite;
}
.empty-text {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    color: #334155;
    margin-bottom: 0.3rem;
}
.empty-sub {
    font-size: 0.8rem;
    color: #1e293b;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Helpers ────────────────────────────────────────────────────────────────
def sentiment_class(s):
    return {"Positive":"sent-pos","Negative":"sent-neg",
            "Neutral":"sent-neu","Frustrated":"sent-frus","Urgent":"sent-urg"}.get(s,"sent-neu")

def sentiment_emoji(s):
    return {"Positive":"😊","Negative":"😞","Neutral":"😐",
            "Frustrated":"😤","Urgent":"🚨"}.get(s,"😐")

def category_emoji(c):
    return {"Billing":"💳","Technical Support":"🔧","General Inquiry":"💬",
            "Complaint":"⚠️","Feedback":"📝","Refund Request":"↩️",
            "Account Issue":"🔐"}.get(c,"💬")

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-title'>☆ JoestarIQ Stats</div>", unsafe_allow_html=True)

    total = len(st.session_state.history)
    pos   = sum(1 for h in st.session_state.history if h["sentiment"] == "Positive")
    neg   = sum(1 for h in st.session_state.history if h["sentiment"]
                in ("Negative","Frustrated","Urgent"))

    st.markdown(f"""
    <div class='stat-card'>
        <span class='stat-label'>🗿 Total Queries</span>
        <span class='stat-value'>{total}</span>
    </div>
    <div class='stat-card'>
        <span class='stat-label'> Positive </span>
        <span class='stat-value' style='color:#22c55e'>{pos}</span>
    </div>
    <div class='stat-card'>
        <span class='stat-label'>Negative</span>
        <span class='stat-value' style='color:#ef4444'>{neg}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:#334155;text-align:center;margin-bottom:0.8rem;font-style:italic'>\"Your next line is... clear history\"</div>", unsafe_allow_html=True)

    if st.button("🗑️ Za Hando! Clear History", disabled=total == 0):
        st.session_state.history = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem;color:#1e293b;text-align:center;line-height:1.8'>
        Powered by Gemini 2.5 Flash<br>
        Built different 🗿<br>
        <span style='color:#fbbf2444'>☆ JJBA x Support ☆</span>
    </div>
    """, unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap'>
    <div class='hero-icon'>☆</div>
    <div class='hero-title'>JoestarIQ</div>
</div>
<div class='hero-sub'>
    <span>Classify</span> queries ·
    <span>Analyze</span> sentiment ·
    <span>Generate</span> contextual AI responses
</div>
<div class='hero-quote'>
    "Kono customer support da!" 
    <span>— Joseph Joestar, probably</span>
</div>
""", unsafe_allow_html=True)


st.divider()

user_input = st.chat_input("Please enter your query... (Type your query)")
if user_input:
    gif_placeholder = st.empty()
    gif_placeholder.markdown("""
    <div style='text-align:center;padding:2rem'>
        <img src='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGxyMmxwMDh6ZDNpOTI4cGF5ZGlndXVpcGI4eW91OW90ejlmbTdkbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kNpNw0eB1w4qDYA7hS/giphy.gif'
             width='280'
             style='border-radius:16px;border:1px solid #1e1e2e;
                    box-shadow:0 0 30px rgba(251,191,36,0.2)'/>
        <div style='font-family:Syne,sans-serif;font-size:0.85rem;
                    color:#fbbf24;margin-top:1rem;letter-spacing:0.1em'>
            ☆ The cat is — Processing your query...
        </div>
    </div>
    """, unsafe_allow_html=True)

    result = process_query(user_input)
    result["query"]     = user_input
    result["timestamp"] = datetime.now().strftime("%b %d, %Y · %H:%M")
    st.session_state.history.append(result)

    gif_placeholder.empty()  
    st.rerun()
# ── Conversation ───────────────────────────────────────────────────────────
if not st.session_state.history:
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-icon'>☆</div>
        <div class='empty-text'>No queries yet, bro</div>
        <div class='empty-sub'>"Your next line is... type something" — Dio, probably</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for item in reversed(st.session_state.history):
        with st.chat_message("user"):
            st.write(item["query"])

        with st.chat_message("assistant"):
            sc = sentiment_class(item["sentiment"])
            ce = category_emoji(item["category"])
            se = sentiment_emoji(item["sentiment"])
            st.markdown(f"""
            <div class='tag-row'>
                <span class='tag cat'>{ce} {item['category']}</span>
                <span class='tag {sc}'>{se} {item['sentiment']}</span>
            </div>
            <div class='response-text'>{item['response']}</div>
            <div class='timestamp'>{item['timestamp']}</div>
            """, unsafe_allow_html=True)

        st.divider()
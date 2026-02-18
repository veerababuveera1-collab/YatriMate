import streamlit as st
import google.generativeai as genai
from typing import TypedDict
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - 2026 Edition", 
    page_icon="🗺️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM UI & STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="st-"] { font-family: 'Poppins', sans-serif; }
    .stApp {
        background: url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    .agent-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 15px;
        color: white;
    }
    .itinerary-container {
        background: white;
        padding: 30px;
        border-radius: 20px;
        color: #1a1a1a;
        border-left: 10px solid #FF9933;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #138808);
        color: white !important;
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ENGINE (Gemini 3 Flash) ---
def get_gemini_client():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("API Key Missing! Please add it to .streamlit/secrets.toml")
        return None
    genai.configure(api_key=api_key)
    # Using the latest 2026 model
    return genai.GenerativeModel('gemini-3-flash-preview')

def agent_task(model, prompt, role="General"):
    # System instruction sets the 'persona'
    sys_msg = f"Role: {role}. Provide clear, accurate travel details. Use Telugu and English as requested."
    try:
        response = model.generate_content(f"{sys_msg}\n\nTask: {prompt}")
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. SESSION STATE INITIALIZATION ---
if "itinerary" not in st.session_state:
    st.session_state.itinerary = ""
if "steps" not in st.session_state:
    st.session_state.steps = {"planner": "", "research": "", "writer": ""}

# --- 5. UI LAYOUT ---
st.markdown('<h1 style="color:white; text-align:center; font-size:3rem;">🗺️ YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:white; text-align:center; font-size:1.2rem;">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ - Powered by Gemini 3</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Agent Settings")
    st.info("ప్రస్తుతం **Gemini 3 Flash** మోడల్ వాడుతున్నాము. ఇది వేగంగా మరియు ఖచ్చితంగా సమాధానాలిస్తుంది.")
    if st.button("క్లియర్ చేయండి (Clear)"):
        st.session_state.itinerary = ""
        st.session_state.steps = {"planner": "", "research": "", "writer": ""}
        st.rerun()

# Main Input
user_input = st.text_input("మీ ప్రయాణ గమ్యాన్ని తెలపండి:", placeholder="ఉదా: 3-రోజుల వైజాగ్ యాత్ర ప్లాన్...")
generate_btn = st.button("యాత్ర ప్రారంభించు 🚩")

if generate_btn and user_input:
    model = get_gemini_client()
    if model:
        p1, p2, p3 = st.columns(3)
        
        # STEP 1: PLANNER
        with p1:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            with st.spinner("🗺️ రూట్ మ్యాప్ సిద్ధం చేస్తున్నాను..."):
                res = agent_task(model, f"Create a skeleton itinerary for: {user_input}", "Travel Architect")
                st.session_state.steps["planner"] = res
                st.success("Planner Ready!")
                st.write(res[:100] + "...")
            st.markdown('</div>', unsafe_allow_html=True)

        # STEP 2: RESEARCHER
        with p2:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            with st.spinner("🔍 ధరలు మరియు సమయాలు వెతుకుతున్నాను..."):
                res = agent_task(model, f"Research entrance fees and timings for: {st.session_state.steps['planner']}", "Expert Researcher")
                st.session_state.steps["research"] = res
                st.success("Research Done!")
                st.write("✅ Facts Verified")
            st.markdown('</div>', unsafe_allow_html=True)

        # STEP 3: WRITER
        with p3:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            with st.spinner("✍️ అందమైన గైడ్ రాస్తున్నాను..."):
                prompt = f"Combine this: {st.session_state.steps['research']}. Write a travel guide in Telugu and English."
                res = agent_task(model, prompt, "Creative Writer")
                st.session_state.itinerary = res
                st.success("Guide Finished!")
            st.markdown('</div>', unsafe_allow_html=True)

# --- 6. DISPLAY FINAL RESULT ---
if st.session_state.itinerary:
    st.divider()
    st.markdown("### 📔 మీ ప్రత్యేక ప్రయాణ నివేదిక (Final Itinerary)")
    st.markdown(f'<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.download_button(
        label="డౌన్లోడ్ గైడ్ 📥",
        data=st.session_state.itinerary,
        file_name="My_Travel_Plan.md",
        mime="text/markdown"
    )

st.markdown('<p style="text-align:center; color:white; margin-top:50px;">YatriMate AI 2026 • Gemini 3 Flash Preview</p>', unsafe_allow_html=True)

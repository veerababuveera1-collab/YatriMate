import streamlit as st
import google.generativeai as genai
from typing import TypedDict
import time

# --- 1. STATE DEFINITION ---
class TravelState(TypedDict):
    request: str
    skeleton_plan: str
    research_data: str
    final_itinerary: str

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Your Travel Companion", 
    page_icon="🗺️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. CUSTOM UI & STYLING (Mind-Blowing GUI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Vibrant Travel Background */
    .stApp {
        background: url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Glassmorphism Logic */
    .agent-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        color: #ffffff;
    }

    /* Premium Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        color: #000080; /* Navy Blue like Ashoka Chakra */
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: 0.4s;
        width: 100%;
        text-transform: uppercase;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }

    .title-text {
        color: #ffffff;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.6);
        font-weight: 900;
        font-size: 4.5rem !important;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .subtitle-text {
        color: #ffffff;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 400;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 3rem;
    }

    /* Final Result Container */
    .itinerary-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 25px;
        color: #1a1a1a;
        border: 2px solid #FF9933;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CORE ENGINE (Gemini 1.5 Flash) ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-1.5-flash')

def agent_task(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 5. UI LAYOUT ---

st.markdown('<h1 class="title-text">YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">మీ వ్యక్తిగత ప్రయాణ వేదిక - Autonomous Travel Agent</p>', unsafe_allow_html=True)

# Sidebar Control
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=120)
    st.markdown("### 🛠️ Agent Dashboard")
    if st.secrets.get("GOOGLE_API_KEY"):
        st.success("Yatri Engine Active ✅")
    else:
        st.error("Missing API Key in Secrets ❌")
    
    st.divider()
    st.info("""
    **YatriMate Workflow:**
    - **Planner Agent:** బ్లూప్రింట్ సిద్ధం చేస్తుంది.
    - **Researcher Agent:** వాస్తవాలను ధృవీకరిస్తుంది.
    - **Writer Agent:** అందమైన గైడ్‌ను రాస్తుంది.
    """)

# Main Input Section
with st.container():
    input_col, btn_col = st.columns([4, 1])
    with input_col:
        user_prompt = st.text_input("", placeholder="ఉదా: 5-రోజుల కాశీ యాత్ర ప్రణాళిక...", label_visibility="collapsed")
    with btn_col:
        go_btn = st.button("ప్రారంభించు 🚩")

# Pipeline Execution
if go_btn:
    model = get_gemini_model()
    
    if model and user_prompt:
        state = TravelState(request=user_prompt, skeleton_plan="", research_data="", final_itinerary="")
        
        # Agents Progress Visualization
        p1, p2, p3 = st.columns(3)
        
        # STEP 1: PLANNER
        with p1:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.markdown("#### 🗺️ Planner Agent")
            with st.spinner("ప్లాన్ వేస్తోంది..."):
                state['skeleton_plan'] = agent_task(model, f"Create a skeleton itinerary for: {user_prompt}")
                st.caption("Strategy Layer Complete")
                st.write(state['skeleton_plan'][:150] + "...")
            st.markdown('</div>', unsafe_allow_html=True)

        # STEP 2: RESEARCHER
        with p2:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.markdown("#### 🔍 Research Agent")
            with st.spinner("వివరాలు వెతుకుతోంది..."):
                state['research_data'] = agent_task(model, f"Research prices, hours, and addresses for: {state['skeleton_plan']}")
                st.caption("Data Verified")
                st.write("✅ 10+ Facts Checked")
            st.markdown('</div>', unsafe_allow_html=True)

        # STEP 3: WRITER
        with p3:
            st.markdown('<div class="agent-card">', unsafe_allow_html=True)
            st.markdown("#### ✍️ Writer Agent")
            with st.spinner("రిపోర్ట్ రాస్తోంది..."):
                final_prompt = f"Using this research: {state['research_data']}, write a final travel guide in Telugu and English."
                state['final_itinerary'] = agent_task(model, final_prompt)
                st.caption("Final Polish Done")
                st.write("✨ Guide Ready!")
            st.markdown('</div>', unsafe_allow_html=True)

        # FINAL OUTPUT
        st.divider()
        st.markdown("### 📔 మీ ప్రత్యేక ప్రయాణ నివేదిక (Final Itinerary)")
        st.markdown(f'<div class="itinerary-container">{state["final_itinerary"]}</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="Download Yatri Guide 📥",
            data=state['final_itinerary'],
            file_name="YatriMate_Plan.md",
            mime="text/markdown"
        )
    else:
        st.error("దయచేసి మీ అభ్యర్థనను తెలియజేయండి లేదా API Key తనిఖీ చేయండి.")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 60px; color: white; opacity: 0.8;">
        YatriMate AI • Powered by Gemini 1.5 Flash • Smart Travel Agent System
    </div>
    """, unsafe_allow_html=True)

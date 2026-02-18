import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CORE ARCHITECTURE ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Main Container Cleanup */
    .stApp { background-color: #f8fafc; }

    /* Split Screen Concept from image_789a1f.jpg */
    .main-canvas {
        display: flex;
        background: white;
        border-radius: 40px;
        overflow: hidden;
        box-shadow: 0 50px 100px rgba(0,0,0,0.1);
        max-width: 1100px;
        margin: 50px auto;
        height: 650px;
    }

    /* Left Side - The Travel Experience */
    .left-panel {
        flex: 1.2;
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1503220317375-aaad61436b1b?auto=format&fit=crop&w=1000&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 50px;
        color: white;
        text-align: center;
    }

    .quote-box {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.3;
        text-transform: uppercase;
        border-top: 3px solid #3b82f6;
        border-bottom: 3px solid #3b82f6;
        padding: 30px 0;
    }

    /* Right Side - Premium Dashboard/Login */
    .right-panel {
        flex: 1;
        background: #0f172a; /* Deep Travel Night Blue */
        padding: 60px 45px;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .brand-text { font-size: 3rem; font-weight: 800; margin-bottom: 5px; color: white; }
    .tagline { color: #94a3b8; font-size: 1.1rem; margin-bottom: 40px; }

    /* Form Styling */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        height: 55px;
        padding-left: 20px;
    }

    /* Action Button */
    div.stButton > button {
        background: white !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        border-radius: 30px !important;
        height: 55px;
        width: 100%;
        border: none;
        transition: 0.3s ease;
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(255,255,255,0.1); }

    /* Results Card */
    .result-card {
        background: white;
        color: #1e293b;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        line-height: 1.8;
        border-left: 10px solid #3b82f6;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI SYSTEM ---
def call_travel_agents(query):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel Planner for: {query}.
        Structure your response with:
        1. 🗺️ Route Architect: Scenic path & stopovers.
        2. 🗓️ Master Planner: Day-wise detailed activities.
        3. 🥘 Culture Expert: Top 3 local dishes & estimated budget in INR.
        Language: English & Telugu Mix. Use professional Markdown.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "🚨 API Connection Issue. Please verify st.secrets."

# --- 4. APP LOGIC ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# --- 5. THE LOGIN INTERFACE (Side-by-Side) ---
if not st.session_state.auth:
    # Creating a faux split container using Streamlit columns
    _, center_col, _ = st.columns([0.1, 2, 0.1])
    with center_col:
        st.markdown(f"""
            <div class="main-canvas">
                <div class="left-panel">
                    <div class="quote-box">"Travel is the only thing<br>you buy that makes<br>you richer"</div>
                </div>
                <div class="right-panel">
        """, unsafe_allow_html=True)
        
        # Real Streamlit Input Elements overlayed in the Right Panel logic
        st.markdown('<div class="brand-text">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="tagline">Your AI Compass for Every Horizon</div>', unsafe_allow_html=True)
        
        email = st.text_input("Traveler Email", placeholder="veera@traveler.com", label_visibility="collapsed")
        pwd = st.text_input("Access Key", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        if st.button("UNLOCK ACCESS 🚀"):
            if email == "veera@traveler.com" and pwd == "buddy_password_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- 6. THE TRAVELER DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("### 🧭 YatriMate AI")
        if st.button("Logout 🚪"):
            st.session_state.auth = False
            st.session_state.itinerary = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:#0f172a; margin-top:30px;'>Where to next, Traveler?</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        query = st.text_input("", placeholder="Enter destination (e.g., Hyderabad to Munnar)", label_visibility="collapsed")
        if st.button("PLAN MY JOURNEY 🚀"):
            if query:
                with st.status("🔮 Coordinating AI Agents...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    st.write("🗓️ Planner is scheduling days...")
                    res = call_travel_agents(query)
                    st.session_state.itinerary = res
                    s.update(label="Itinerary Ready!", state="complete")

    if st.session_state.itinerary:
        st.markdown(f'<div class="result-card">{st.session_state.itinerary}</div>', unsafe_allow_html=True)
        if st.button("🔄 Start New Plan"):
            st.session_state.itinerary = None
            st.rerun()

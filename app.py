import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI ENGINE (Professional Background & Zero-Box Design) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Scenic Professional Traveling Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.4)), 
                    url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Removing Streamlit default container boxes for branding */
    [data-testid="stVerticalBlock"] > div:has(div.brand-h1) {
        background: transparent !important;
        padding: 0px !important;
        border: none !important;
    }

    /* Floating Branding - No Boxes */
    .brand-h1 { 
        font-size: 5rem; 
        font-weight: 800; 
        letter-spacing: -3px; 
        margin-bottom: 0px;
        color: #ffffff;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
    }
    .brand-tag { 
        font-size: 1.3rem; 
        opacity: 0.95; 
        font-weight: 300; 
        margin-top: -10px;
        margin-bottom: 40px;
        color: #ffffff;
        text-shadow: 0 4px 15px rgba(0,0,0,0.4);
        text-align: center;
    }

    /* Elegant Glassmorphism Card */
    .login-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 55px 45px;
        border-radius: 40px;
        max-width: 480px;
        margin: auto;
        box-shadow: 0 50px 100px rgba(0,0,0,0.5);
        text-align: center;
        color: white;
    }

    /* Inputs & Buttons */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 18px !important;
        height: 60px;
        font-size: 1.1rem;
        border: none !important;
    }

    div.stButton > button {
        background: #2563eb !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 18px !important;
        height: 60px;
        width: 100%;
        border: none;
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4);
        transition: 0.4s;
    }
    div.stButton > button:hover { transform: translateY(-3px); background: #1d4ed8 !important; }

    /* Itinerary Box */
    .itinerary-container {
        background: rgba(255, 255, 255, 0.98);
        padding: 40px;
        border-radius: 30px;
        color: #0f172a;
        margin-top: 40px;
        border-left: 15px solid #2563eb;
        line-height: 1.8;
        box-shadow: 0 30px 60px rgba(0,0,0,0.4);
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI SYSTEM ---
def run_yatri_agents(query):
    try:
        # Note: Ensure GOOGLE_API_KEY is set in your Streamlit Secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a Professional Multi-Agent Travel Engine for: {query}.
        Structure response with:
        1. 🧭 Route Architect: Scenic stops and best path.
        2. 📅 Master Planner: Day-wise schedule.
        3. 🥘 Culture Expert: Local food tips and budget (INR).
        Language: English & Telugu Mix. 
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "🚨 AI System Offline: Please check API Key in Secrets."

# --- 4. SESSION MANAGEMENT ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'plan' not in st.session_state:
    st.session_state.plan = None

# --- 5. THE INTERFACE ---
if not st.session_state.auth:
    _, mid_col, _ = st.columns([1, 2, 1])
    
    with mid_col:
        # Floating Branding
        st.markdown('<div class="brand-h1">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tag">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        # Glass Login Card
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        u_email = st.text_input("Username", placeholder="veera@traveler.com", label_visibility="collapsed")
        u_pass = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        if st.button("SIGN IN 🚀"):
            if u_email == "veera@traveler.com" and u_pass == "buddy_password_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid credentials.")

        st.markdown('<div style="margin: 25px 0; opacity: 0.5;">━━━━ or ━━━━</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.button("Google 🌐", use_container_width=True)
        with c2: st.button("Apple 🍎", use_container_width=True)
        
        st.markdown('<div style="margin-top: 30px; font-size: 0.9rem;">New Traveler? <b>Join the Club</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Authenticated Dashboard
    with st.sidebar:
        st.title("🧭 YatriMate")
        if st.button("Logout 🚪"):
            st.session_state.auth = False
            st.session_state.plan = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3.5rem; margin-top:50px;'>Where Shall We Explore?</h1>", unsafe_allow_html=True)
    
    _, search_col, _ = st.columns([1, 2, 1])
    with search_col:
        query = st.text_input("", placeholder="e.g., Hyderabad to Munnar", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if query:
                with st.status("🔮 Coordinating AI Agents...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping paths...")
                    time.sleep(1)
                    res = run_yatri_agents(query)
                    st.session_state.plan = res
                    s.update(label="Full Plan Ready!", state="complete")

    if st.session_state.plan:
        st.markdown(f'<div class="itinerary-container">{st.session_state.plan}</div>', unsafe_allow_html=True)
        if st.button("🔄 Start New Journey"):
            st.session_state.plan = None
            st.rerun()

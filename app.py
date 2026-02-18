import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI ENGINE (Professional Nature Background & Zero-Box Design) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* New Professional High-Res Travel Background (Mountain Range) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.4)), 
                    url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Removing all default Streamlit boxes for branding clarity */
    [data-testid="stVerticalBlock"] > div:has(div.brand-h1) {
        background: transparent !important;
        padding: 0px !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Floating Branding - Clean & Modern (No Boxes) */
    .brand-h1 { 
        font-size: 5rem; 
        font-weight: 800; 
        letter-spacing: -3px; 
        margin-bottom: 0px;
        color: #ffffff;
        text-shadow: 0 10px 30px rgba(0,0,0,0.6);
        text-align: center;
    }
    .brand-tag { 
        font-size: 1.3rem; 
        opacity: 0.95; 
        font-weight: 300; 
        margin-top: -10px;
        margin-bottom: 45px;
        color: #ffffff;
        text-shadow: 0 4px 15px rgba(0,0,0,0.4);
        text-align: center;
    }

    /* Premium Glassmorphism Login Card */
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

    /* Field Inputs Styling */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 18px !important;
        height: 60px;
        font-size: 1.1rem;
        border: none !important;
    }

    /* Main Action Button */
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

    /* Itinerary Result Container */
    .itinerary-box {
        background: rgba(255, 255, 255, 0.98);
        padding: 40px;
        border-radius: 30px;
        color: #0f172a;
        margin-top: 40px;
        border-left: 15px solid #2563eb;
        line-height: 1.8;
        box-shadow: 0 35px 70px rgba(0,0,0,0.5);
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI SYSTEM ---
def run_yatri_agents(query):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Role: Senior Multi-Agent Travel Consultant for: {query}.
        Structure response with professional Markdown:
        1. 🗺️ Route Architect: Scenic paths and transit tips.
        2. 📅 Master Planner: Hourly detailed itinerary.
        3. 🍲 Culture Expert: Must-try local dishes and budget estimates (INR).
        Language: Blend of English and Telugu for better context.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "🚨 AI System Offline: Please check your GOOGLE_API_KEY in Streamlit Secrets."

# --- 4. SESSION MANAGEMENT ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'final_itinerary' not in st.session_state:
    st.session_state.final_itinerary = None

# --- 5. THE INTERFACE ---
if not st.session_state.auth:
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        # BRANDING (No Boxes, Just Text)
        st.markdown('<div class="brand-h1">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tag">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        # LOGIN SECTION
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        u_email = st.text_input("Username", placeholder="veera@traveler.com", label_visibility="collapsed")
        u_pass = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        if st.button("SIGN IN 🚀"):
            if u_email == "veera@traveler.com" and u_pass == "buddy_password_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Username or Password.")

        st.markdown('<div style="margin: 25px 0; opacity: 0.5;">━━━━ or continue with ━━━━</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.button("Google 🌐", use_container_width=True)
        with c2: st.button("Apple 🍎", use_container_width=True)
        
        st.markdown('<div style="margin-top: 30px; font-size: 0.95rem;">New Traveler? <b>Create Account</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- DASHBOARD (AFTER LOGIN) ---
    with st.sidebar:
        st.title("🧭 YatriMate AI")
        if st.button("Logout 🚪"):
            st.session_state.auth = False
            st.session_state.final_itinerary = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3.5rem; margin-top:50px; text-shadow: 0 5px 20px rgba(0,0,0,0.5);'>Where Shall We Explore?</h1>", unsafe_allow_html=True)
    
    _, search_col, _ = st.columns([1, 2, 1])
    with search_col:
        query = st.text_input("", placeholder="Enter destination (e.g., Delhi to Ladakh)", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🛸"):
            if query:
                with st.status("🔮 Coordinating AI Intelligence...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    res = run_yatri_agents(query)
                    st.session_state.final_itinerary = res
                    s.update(label="Full Journey Plan Ready!", state="complete")

    if st.session_state.final_itinerary:
        st.markdown(f'<div class="itinerary-box">{st.session_state.final_itinerary}</div>', unsafe_allow_html=True)
        if st.button("🔄 Start New Journey"):
            st.session_state.final_itinerary = None
            st.rerun()

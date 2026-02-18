import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CORE ARCHITECTURAL CONFIG ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM UX/UI ENGINE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Breathtaking High-Res Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1506929113670-b4364b630132?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Glassmorphism Login Container */
    .login-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 50px 45px;
        border-radius: 35px;
        max-width: 480px;
        margin: auto;
        margin-top: 5vh;
        box-shadow: 0 40px 100px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
    }

    /* Branding & Typography */
    .brand-h1 { font-size: 3.2rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 5px; }
    .brand-tag { font-size: 1.1rem; opacity: 0.9; font-weight: 300; margin-bottom: 40px; }

    /* Minimalist Field Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        height: 55px;
        border: none !important;
        font-size: 1.1rem;
    }

    /* Primary CTA Button */
    div.stButton > button {
        background: #2563eb !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        height: 55px;
        width: 100%;
        border: none;
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.3);
        transition: 0.4s ease;
    }
    div.stButton > button:hover { transform: translateY(-3px); background: #1d4ed8 !important; }

    /* Social Buttons */
    .social-btn {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 12px;
        border-radius: 10px;
        margin-top: 10px;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        font-weight: 600;
    }

    /* Links */
    .link-text { font-size: 0.95rem; margin-top: 20px; color: white; opacity: 0.8; cursor: pointer; text-decoration: none;}
    .link-text:hover { opacity: 1; text-decoration: underline; }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_yatri_agents(query):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a Professional Multi-Agent Travel Intelligence for: {query}.
        Structure response with:
        1. 🧭 Route Architect: Scenic paths and midway stops.
        2. 📅 Master Planner: Hourly day-wise itinerary.
        3. 🥘 Culture Expert: 3 must-try local foods and budget in INR.
        Language: English & Telugu Mix. 
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 System Error: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'itinerary_output' not in st.session_state:
    st.session_state.itinerary_output = None

# --- 5. HIGH-CONVERTING LOGIN PAGE ---
if not st.session_state.logged_in:
    _, col_auth, _ = st.columns([1, 1.5, 1])
    
    with col_auth:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="brand-h1">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tag">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        # Inputs
        u_name = st.text_input("Username", placeholder="veera@traveler.com", label_visibility="collapsed")
        u_pass = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        # Forgot Password Link
        st.markdown('<div style="text-align: right; margin-bottom: 20px;"><a href="#" class="link-text">Forgot Password?</a></div>', unsafe_allow_html=True)
        
        if st.button("SIGN IN 🚀"):
            if u_name == "veera@traveler.com" and u_pass == "buddy_password_2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied. Please check your credentials.")

        # Social Logins
        st.markdown('<div style="margin: 25px 0; opacity: 0.6;">━━━━ or continue with ━━━━</div>', unsafe_allow_html=True)
        s_col1, s_col2 = st.columns(2)
        with s_col1: st.button("Google 🌐", key="google")
        with s_col2: st.button("Apple 🍎", key="apple")

        # Create Account CTA
        st.markdown('<div class="link-text" style="margin-top: 30px;">Don\'t have an account? <a href="#" style="color:white; font-weight:700;">Create an Account</a></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AGENT DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("### 🧭 YatriMate AI")
        st.write("Logged in as: **Explorer**")
        if st.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.itinerary_output = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3.5rem; margin-top:40px;'>Curate Your Next Adventure</h1>", unsafe_allow_html=True)
    
    _, col_search, _ = st.columns([1, 2, 1])
    with col_search:
        query = st.text_input("", placeholder="Where would you like to go? (e.g., Delhi to Leh)", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if query:
                with st.status("🔮 Coordinating Travel Intelligence...", expanded=True) as status:
                    st.write("🕵️ Route Architect is mapping paths...")
                    time.sleep(1)
                    res = run_yatri_agents(query)
                    st.session_state.itinerary_output = res
                    status.update(label="Full Plan Ready!", state="complete")

    if st.session_state.itinerary_output:
        st.markdown(f"""
        <div style="background:white; padding:45px; border-radius:30px; color:#0f172a; line-height:1.8; margin-top:40px; border-left: 15px solid #2563eb; box-shadow: 0 30px 60px rgba(0,0,0,0.3);">
            {st.session_state.itinerary_output}
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 New Journey"):
            st.session_state.itinerary_output = None
            st.rerun()

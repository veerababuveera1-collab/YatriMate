import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CORE ARCHITECTURE CONFIG ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI ENGINE (Santorini Sunset & Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Breathtaking High-Res Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.2)), 
                    url('https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Glassmorphism Login Container */
    .login-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 50px 40px;
        border-radius: 35px;
        max-width: 480px;
        margin: auto;
        margin-top: 5vh;
        box-shadow: 0 40px 100px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
    }

    /* Branding & Typography */
    .brand-main { font-size: 3.5rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0px; }
    .brand-tag { font-size: 1.1rem; opacity: 0.9; font-weight: 300; margin-bottom: 40px; }

    /* Modern Responsive Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 14px !important;
        height: 55px;
        border: none !important;
        font-size: 1.1rem;
    }

    /* Prominent Sign In Button */
    div.stButton > button {
        background: #2563eb !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        height: 55px;
        width: 100%;
        border: none;
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4);
        transition: 0.4s ease;
    }
    div.stButton > button:hover { transform: translateY(-3px); background: #1d4ed8 !important; }

    /* Social Divider & CTA */
    .social-divider { margin: 30px 0; opacity: 0.6; font-size: 0.9rem; }
    .footer-links { font-size: 0.95rem; margin-top: 25px; color: white; opacity: 0.8; }
    .footer-links a { color: white; text-decoration: none; font-weight: 700; }

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
        Act as a Professional Multi-Agent Travel Engine for: {query}.
        Structure response with icons:
        1. 🧭 Route Architect: Scenic stops and best path.
        2. 📅 Master Planner: Day-wise schedule.
        3. 🥘 Culture Expert: Local food tips and budget (INR).
        Language: English & Telugu Mix. Professional Markdown.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "🚨 AI System Offline: Please check GOOGLE_API_KEY in Streamlit Secrets."

# --- 4. SESSION MANAGEMENT ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'plan' not in st.session_state:
    st.session_state.plan = None

# --- 5. THE MODERN LOGIN INTERFACE ---
if not st.session_state.auth:
    _, col_main, _ = st.columns([1, 1.4, 1])
    
    with col_main:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="brand-main">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tag">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        # User Fields
        u_email = st.text_input("Username", placeholder="veera@traveler.com", label_visibility="collapsed")
        u_pass = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        # Forgot Password
        st.markdown('<div style="text-align: right; margin-bottom: 20px;"><a href="#" style="color:white; font-size:0.9rem; opacity:0.8;">Forgot Password?</a></div>', unsafe_allow_html=True)
        
        if st.button("SIGN IN 🚀"):
            if u_email == "veera@traveler.com" and u_pass == "buddy_password_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied. Please check your credentials.")

        # Social Login Options
        st.markdown('<div class="social-divider">━━━━ or continue with ━━━━</div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1: st.button("Google 🌐", key="google_login")
        with s2: st.button("Apple 🍎", key="apple_login")

        # Create Account Call-to-Action
        st.markdown('<div class="footer-links">Don\'t have an account? <a href="#">Create an Account</a></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AGENT DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("### 🧭 YatriMate AI")
        st.info("Status: Authenticated")
        if st.button("Logout 🚪"):
            st.session_state.auth = False
            st.session_state.plan = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3rem; margin-top:40px;'>Curate Your Next Horizon</h1>", unsafe_allow_html=True)
    
    _, col_search, _ = st.columns([1, 2, 1])
    with col_search:
        query = st.text_input("", placeholder="Enter your destination (e.g., Hyderabad to Munnar)", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if query:
                with st.status("🔮 Coordinating AI Intelligence...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    res = run_yatri_agents(query)
                    st.session_state.plan = res
                    s.update(label="Full Plan Ready!", state="complete")

    if st.session_state.plan:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.98); padding:40px; border-radius:25px; color:#0f172a; margin-top:40px; border-left: 15px solid #2563eb; line-height:1.8; box-shadow: 0 30px 60px rgba(0,0,0,0.3);">
            {st.session_state.plan}
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 New Search"):
            st.session_state.plan = None
            st.rerun()

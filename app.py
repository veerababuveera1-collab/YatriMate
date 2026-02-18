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

# --- 2. LUXURY DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Breathtaking Background Setup */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Premium Glassmorphism Container */
    .login-container {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 60px 50px;
        border-radius: 40px;
        max-width: 480px;
        margin: auto;
        margin-top: 5vh;
        box-shadow: 0 50px 100px rgba(0,0,0,0.4);
        text-align: center;
        color: white;
    }

    /* Branding Typography */
    .brand-title { font-size: 3.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0px; line-height: 1; }
    .brand-tagline { font-size: 1.1rem; opacity: 0.9; font-weight: 300; margin-bottom: 45px; }

    /* Minimalist Inputs Overrides */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 16px !important;
        height: 58px;
        font-size: 1.1rem;
        border: none !important;
    }

    /* Sign In Button Styling */
    div.stButton > button {
        background: #2563eb !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        height: 58px;
        width: 100%;
        border: none;
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4);
        transition: 0.4s ease;
    }
    div.stButton > button:hover { transform: translateY(-3px); background: #1d4ed8 !important; }

    /* Social Links & Footers */
    .social-divider { margin: 30px 0; opacity: 0.6; font-size: 0.9rem; }
    .footer-link { color: white; text-decoration: none; font-weight: 700; opacity: 0.8; }
    .footer-link:hover { opacity: 1; text-decoration: underline; }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI SYSTEM ---
def call_yatri_agents(query):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Role: Senior Travel Consultant for: {query}.
        Act as 3 AI Agents:
        1. 🧭 Route Architect: Scenic paths & transportation.
        2. 📅 Master Planner: Hourly detailed itinerary.
        3. 🥘 Culture Expert: Top dishes & budget in INR.
        Language: Professional English & Telugu Mix.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "🚨 API Key error. Please check your st.secrets."

# --- 4. SESSION MANAGEMENT ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# --- 5. THE MODERN LOGIN INTERFACE ---
if not st.session_state.auth:
    _, col_center, _ = st.columns([1, 1.4, 1])
    
    with col_center:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="brand-title">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tagline">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        email = st.text_input("Username", placeholder="veera@traveler.com", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        st.markdown('<div style="text-align: right; margin-bottom: 25px;"><a href="#" class="footer-link" style="font-weight:400; font-size:0.9rem;">Forgot Password?</a></div>', unsafe_allow_html=True)
        
        if st.button("SIGN IN 🚀"):
            if email == "veera@traveler.com" and password == "buddy_password_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied. Check credentials.")

        st.markdown('<div class="social-divider">━━━━ or continue with ━━━━</div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1: st.button("Google 🌐", use_container_width=True)
        with s2: st.button("Apple 🍎", use_container_width=True)

        st.markdown('<div style="margin-top: 35px; font-size: 0.95rem;">New to YatriMate? <a href="#" class="footer-link">Create Account</a></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. THE TRAVELER DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("### 🧭 YatriMate AI")
        if st.button("Logout 🚪"):
            st.session_state.auth = False
            st.session_state.itinerary = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3.5rem; margin-top:50px; text-shadow: 0 4px 12px rgba(0,0,0,0.4);'>Where is your heart leading?</h1>", unsafe_allow_html=True)
    
    _, s_col, _ = st.columns([1, 2, 1])
    with s_col:
        query = st.text_input("", placeholder="e.g., Delhi to Ladakh via Manali", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🛸"):
            if query:
                with st.status("🔮 Coordinating Travel Intelligence...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    res = call_yatri_agents(query)
                    st.session_state.itinerary = res
                    s.update(label="Full Itinerary Ready!", state="complete")

    if st.session_state.itinerary:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.98); padding:45px; border-radius:30px; color:#0f172a; margin-top:45px; border-left: 15px solid #2563eb; line-height:1.8; box-shadow: 0 35px 70px rgba(0,0,0,0.4);">
            {st.session_state.itinerary}
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Start New Journey"):
            st.session_state.itinerary = None
            st.rerun()

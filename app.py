import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE CONFIG ---
st.set_page_config(
    page_title="YatriMate AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Clean Santorini Background - No extra overlays */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.2)), 
                    url('https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Fixed Glassmorphism Login Card */
    .login-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 60px 50px;
        border-radius: 40px;
        max-width: 500px;
        margin: auto;
        margin-top: 10vh; /* Perfectly centered */
        box-shadow: 0 40px 100px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
    }

    /* Clear Branding - No boxes around text */
    .brand-h1 { 
        font-size: 4rem; 
        font-weight: 800; 
        letter-spacing: -2px; 
        margin-bottom: 0px;
        text-shadow: 0 4px 15px rgba(0,0,0,0.4); /* Makes text pop */
    }
    .brand-tag { 
        font-size: 1.2rem; 
        opacity: 0.9; 
        font-weight: 300; 
        margin-bottom: 45px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    /* Clean Modern Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 16px !important;
        height: 58px;
        border: none !important;
        font-size: 1.1rem;
    }

    /* Primary CTA */
    div.stButton > button {
        background: #2563eb !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        height: 58px;
        width: 100%;
        border: none;
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4);
    }

    /* Social Buttons Alignment */
    .stButton > button[kind="secondary"] {
        border-radius: 12px !important;
        height: 50px;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. APP LOGIC ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    _, col_auth, _ = st.columns([1, 1.8, 1])
    
    with col_auth:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        # Project name is now clean and highlighted
        st.markdown('<div class="brand-h1">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tag">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        email = st.text_input("Username", placeholder="veera@traveler.com", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        st.markdown('<div style="text-align: right; margin-bottom: 25px;"><a href="#" style="color:white; opacity:0.8; font-size:0.9rem; text-decoration:none;">Forgot Password?</a></div>', unsafe_allow_html=True)
        
        if st.button("SIGN IN 🚀"):
            if email == "veera@traveler.com" and password == "buddy_password_2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid credentials.")

        st.markdown('<div style="margin: 30px 0; opacity: 0.5;">━━━━ or continue with ━━━━</div>', unsafe_allow_html=True)
        
        s1, s2 = st.columns(2)
        with s1: st.button("Google 🌐", use_container_width=True)
        with s2: st.button("Apple 🍎", use_container_width=True)

        st.markdown('<div style="margin-top: 35px; font-size: 0.95rem;">New Traveler? <a href="#" style="color:white; font-weight:700; text-decoration:none;">Create Account</a></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Dashbaord Logic
    with st.sidebar:
        st.title("🧭 YatriMate AI")
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()
    st.markdown("<h1 style='text-align:center; color:white; margin-top:10vh;'>Welcome, Traveler!</h1>", unsafe_allow_html=True)

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

# --- 2. PROFESSIONAL TRAVEL UI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* New Professional Traveling Background (Scenic Mountains & Explorer) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Elegant Glassmorphism Card */
    .login-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 60px 50px;
        border-radius: 40px;
        max-width: 500px;
        margin: auto;
        margin-top: 8vh;
        box-shadow: 0 50px 100px rgba(0,0,0,0.4);
        text-align: center;
        color: white;
    }

    /* Ultra-Clean Branding - NO EXTRA BOXES */
    .brand-h1 { 
        font-size: 4rem; 
        font-weight: 800; 
        letter-spacing: -2px; 
        margin-bottom: 5px;
        text-shadow: 0 8px 20px rgba(0,0,0,0.5); 
    }
    .brand-tag { 
        font-size: 1.1rem; 
        opacity: 0.9; 
        font-weight: 300; 
        margin-bottom: 45px;
        letter-spacing: 1px;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    /* Minimalist Field Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 16px !important;
        height: 58px;
        border: none !important;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Action Button Styling */
    div.stButton > button {
        background: #2563eb !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        height: 58px;
        width: 100%;
        border: none;
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4);
        transition: all 0.4s ease;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 20px 45px rgba(37, 99, 235, 0.6); }

    /* Social Buttons */
    .stButton > button[kind="secondary"] {
        border-radius: 14px !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI LOGIC ---
def run_travel_agents(query):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a Professional Travel Intelligence System for: {query}.
        Structure:
        1. 🧭 Route Architect: Best transit and scenic paths.
        2. 📅 Master Planner: Day-wise detailed itinerary.
        3. 🥘 Culture Expert: Local food and budget in INR.
        Language: English & Telugu Mix. Professional Markdown.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "🚨 System Error: Check GOOGLE_API_KEY in Secrets."

# --- 4. SESSION & AUTH ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 5. THE PROFESSIONAL LOGIN PAGE ---
if not st.session_state.logged_in:
    _, auth_col, _ = st.columns([1, 1.6, 1])
    
    with auth_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="brand-h1">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tag">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        u_email = st.text_input("Traveler Email", placeholder="veera@traveler.com", label_visibility="collapsed")
        u_pass = st.text_input("Access Key", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        st.markdown('<div style="text-align: right; margin-bottom: 25px;"><a href="#" style="color:white; opacity:0.7; font-size:0.9rem; text-decoration:none;">Forgot Password?</a></div>', unsafe_allow_html=True)
        
        if st.button("SIGN IN 🚀"):
            if u_email == "veera@traveler.com" and u_pass == "buddy_password_2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied.")

        st.markdown('<div style="margin: 25px 0; opacity: 0.5;">━━━━ or continue with ━━━━</div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1: st.button("Google 🌐", key="g", use_container_width=True)
        with s2: st.button("Apple 🍎", key="a", use_container_width=True)

        st.markdown('<div style="margin-top: 35px; font-size: 0.95rem;">New Explorer? <a href="#" style="color:white; font-weight:700; text-decoration:none;">Join the Club</a></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AGENT DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("### 🧭 YatriMate AI")
        if st.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.itinerary_data = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3.5rem; margin-top:50px; text-shadow: 0 5px 15px rgba(0,0,0,0.4);'>Map Your Next Horizon</h1>", unsafe_allow_html=True)
    
    _, search_col, _ = st.columns([1, 2, 1])
    with search_col:
        query = st.text_input("", placeholder="Where would you like to go?", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🛸"):
            if query:
                with st.status("🔮 Coordinating Travel Intelligence...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    res = run_travel_agents(query)
                    st.session_state.itinerary_data = res
                    s.update(label="Full Plan Ready!", state="complete")

    if st.session_state.itinerary_data:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.98); padding:40px; border-radius:30px; color:#0f172a; margin-top:40px; border-left: 15px solid #2563eb; line-height:1.8; box-shadow: 0 30px 60px rgba(0,0,0,0.4);">
            {st.session_state.itinerary_data}
        </div>
        """, unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CINEMATIC TRAVEL UI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Cinematic Background - Road & Mountains */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Main Login Container (Refined Glass) */
    .main-login-container {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 60px 50px;
        border-radius: 30px;
        text-align: center;
        max-width: 700px;
        margin: auto;
        margin-top: 80px;
    }

    /* Branding - Matches your screenshot */
    .brand-title {
        color: #ffffff;
        font-weight: 800;
        font-size: 4.5rem;
        margin-bottom: 0px;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .brand-quote {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.4rem;
        font-weight: 300;
        margin-bottom: 40px;
        font-style: italic;
    }

    /* Input Field Styling */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        border: none !important;
        height: 55px;
        font-size: 1.1rem;
        padding-left: 20px;
    }

    /* Login Button - Neon Glow */
    div.stButton > button {
        background: linear-gradient(90deg, #4f46e5, #9333ea) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 60px;
        width: 100%;
        font-weight: 700;
        font-size: 1.2rem;
        border: none;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.4);
        transition: 0.4s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(147, 51, 234, 0.6);
    }

    /* White Result Paper */
    .itinerary-paper {
        background: #ffffff;
        color: #0f172a;
        padding: 40px;
        border-radius: 25px;
        margin-top: 30px;
        line-height: 1.8;
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
    }

    /* Option Menu Overrides */
    .nav-link { font-weight: 600 !important; color: white !important; }
    .nav-link-selected { background-color: #4f46e5 !important; border-radius: 10px !important; }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI AGENT ENGINE ---
def run_ai_agents(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Role: Luxury Multi-Agent Travel Planner.
        Analyze: {query}. Respond in {lang}.
        Agents:
        1. 🗺️ Route Architect: Best mid-way stops.
        2. 🗓️ Master Planner: Detailed schedule.
        3. 🥘 Culture Expert: Local foods and INR budget.
        Format: Elegant Markdown with icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 API Connection Error: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'plan' not in st.session_state:
    st.session_state.plan = None

# --- 5. LOGIN PAGE (BASED ON YOUR SCREENSHOT) ---
if not st.session_state.auth:
    _, col2, _ = st.columns([0.2, 2, 0.2])
    with col2:
        st.markdown('<div class="main-login-container">', unsafe_allow_html=True)
        st.markdown('<div class="brand-title">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-quote">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)

        mode = option_menu(None, ["Explorer Login", "Join the Club"], 
            icons=['shield-lock', 'person-plus'], orientation="horizontal",
            styles={"container": {"background-color": "rgba(255,255,255,0.1)"}})

        if mode == "Explorer Login":
            st.text_input("Traveler Email", placeholder="veera@traveler.com", key="u_email")
            st.text_input("Secret Access Key", type="password", placeholder="••••••••", key="u_pwd")
            if st.button("Access Dashboard 🚀"):
                st.session_state.auth = True
                st.rerun()
        else:
            st.text_input("Full Name")
            st.text_input("Email ID")
            st.text_input("Create Password", type="password")
            st.button("Register Now ✨")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. DASHBOARD ---
else:
    with st.sidebar:
        st.markdown('### YatriMate AI')
        if st.button("Logout 🚪"):
            st.session_state.auth = False
            st.session_state.plan = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white;'>Map Your Adventure</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        query = st.text_input("", placeholder="Where do you want to go? (e.g. Hyderabad to Varanasi)", label_visibility="collapsed")
        if st.button("TRIGGER AI AGENTS 🚀"):
            if query:
                with st.status("🔮 Coordinating Travel Intelligence...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping stopovers...")
                    time.sleep(1)
                    res = run_ai_agents(query, "English & Telugu Mix")
                    st.session_state.plan = res
                    s.update(label="Full Plan Ready!", state="complete")

    if st.session_state.plan:
        st.markdown(f'<div class="itinerary-paper">{st.session_state.plan}</div>', unsafe_allow_html=True)
        if st.button("🔄 New Search"):
            st.session_state.plan = None
            st.rerun()

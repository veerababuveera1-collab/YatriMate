import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ELITE TRAVELER UI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Cinematic High-Res Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Main Glass Canvas */
    .glass-canvas {
        background: rgba(15, 23, 42, 0.25);
        backdrop-filter: blur(45px);
        -webkit-backdrop-filter: blur(45px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 60px 50px;
        border-radius: 40px;
        text-align: center;
        max-width: 800px;
        margin: auto;
        margin-top: 5vh;
        box-shadow: 0 40px 100px rgba(0,0,0,0.5);
    }

    /* Elegant Branding */
    .hero-title {
        color: #ffffff;
        font-weight: 800;
        font-size: 5.5rem;
        margin-bottom: 0px;
        letter-spacing: -3px;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .hero-quote {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.4rem;
        font-weight: 300;
        margin-bottom: 50px;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    /* Minimalist Field Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.98) !important;
        color: #0f172a !important;
        border-radius: 15px !important;
        height: 60px;
        font-size: 1.2rem;
        border: none !important;
        padding-left: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    /* Premium Action Button */
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 65px;
        width: 100%;
        font-weight: 700;
        font-size: 1.3rem;
        border: none;
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4);
        transition: 0.4s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(139, 92, 246, 0.6);
    }

    /* Clean Result Board */
    .itinerary-paper {
        background: #ffffff;
        color: #0f172a;
        padding: 50px;
        border-radius: 35px;
        border-left: 20px solid #3b82f6;
        margin-top: 40px;
        line-height: 1.8;
        box-shadow: 0 30px 60px rgba(0,0,0,0.4);
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_ai_travel_system(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Role: Senior Multi-Agent Travel Consultant for: {query}.
        Format in {lang} using these 3 specialized outputs:
        1. 🧭 Route Architect: Best scenic route with mid-way stopovers.
        2. 📅 Master Planner: Hourly day-wise itinerary.
        3. 🥘 Culture Expert: 3 must-try local dishes and budget in INR.
        Use professional Markdown with clear icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 System Error: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# --- 5. AUTHENTICATION PAGE ---
if not st.session_state.auth:
    _, col2, _ = st.columns([0.1, 2, 0.1])
    with col2:
        st.markdown('<div class="glass-canvas">', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-quote">Your AI Compass for Every Horizon</div>', unsafe_allow_html=True)

        mode = option_menu(None, ["Explorer Login", "Join the Club"], 
            icons=['key', 'person-plus'], orientation="horizontal",
            styles={"container": {"background-color": "transparent"}, "nav-link": {"color": "white"}})

        if mode == "Explorer Login":
            u_email = st.text_input("", placeholder="Traveler Email", key="login_id")
            u_pwd = st.text_input("", placeholder="Access Key", type="password", key="login_pwd")
            if st.button("Unlock Dashboard 🚀"):
                # Static Credentials for testing: veera@traveler.com | buddy_password_2026
                if u_email == "veera@traveler.com" and u_pwd == "buddy_password_2026":
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try again.")
        else:
            st.text_input("", placeholder="Full Name")
            st.text_input("", placeholder="Email Address")
            st.text_input("", placeholder="Create Access Key", type="password")
            st.button("Begin Journey ✨")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AGENT DASHBOARD ---
else:
    with st.sidebar:
        st.markdown('## 🧭 YatriMate AI')
        st.info("Logged in as Traveler")
        if st.button("Logout 🚪"):
            st.session_state.auth = False
            st.session_state.itinerary = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3.5rem; margin-top:50px;'>Where to next, Traveler?</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        query = st.text_input("", placeholder="e.g., Hyderabad to Varanasi via Nagpur", label_visibility="collapsed")
        if st.button("COMMAND AI AGENTS 🚀"):
            if query:
                with st.status("🔮 Coordinating Intelligence...", expanded=True) as s:
                    st.write("🕵️ Route Architect is calculating paths...")
                    time.sleep(1)
                    res = run_ai_travel_system(query, "English & Telugu Mix")
                    st.session_state.itinerary = res
                    s.update(label="Curation Complete!", state="complete")

    if st.session_state.itinerary:
        st.markdown(f'<div class="itinerary-paper">{st.session_state.itinerary}</div>', unsafe_allow_html=True)
        if st.button("🔄 Plan New Horizon"):
            st.session_state.itinerary = None
            st.rerun()
    else:
        # Subtle Trending Destinations
        st.write("---")
        st.markdown("<h3 style='text-align:center; color:white;'>Trending Destinations</h3>", unsafe_allow_html=True)
        t_cols = st.columns(4)
        dest = [("Varanasi", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"),
                ("Ladakh", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?w=400"),
                ("Andaman", "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"),
                ("Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400")]
        for i, (name, img) in enumerate(dest):
            with t_cols[i]:
                st.image(img, use_container_width=True, caption=name)

    st.markdown("<br><p style='text-align:center; color:#94a3b8;'>© 2026 YatriMate AI | Your AI Compass</p>", unsafe_allow_html=True)

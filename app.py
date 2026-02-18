import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI DESIGN (Direct Match to image_789a1f.jpg) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&display=swap');
    
    * { font-family: 'Montserrat', sans-serif; }

    /* Hide Default Streamlit Clutter */
    header, footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Background Setup */
    .stApp {
        background: #f4f7f9;
    }

    /* Main Split Container */
    .travel-canvas {
        display: flex;
        background: white;
        border-radius: 25px;
        overflow: hidden;
        box-shadow: 0 40px 80px rgba(0,0,0,0.12);
        max-width: 1080px;
        margin: 60px auto;
        height: 620px;
    }

    /* Left Side: Cinematic Visuals & Strong Quote */
    .left-hero {
        flex: 1.2;
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1469854523086-cc02fe5d8dfc?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 60px;
        color: white;
    }

    .quote-style {
        font-size: 1.9rem;
        font-weight: 700;
        text-align: center;
        line-height: 1.4;
        text-transform: uppercase;
        border-top: 3px solid #ffffff;
        border-bottom: 3px solid #ffffff;
        padding: 30px 0;
        letter-spacing: 2px;
    }

    /* Right Side: Professional Midnight Blue Login */
    .right-auth {
        flex: 1;
        background: #102a43; /* Exact Deep Blue */
        padding: 70px 50px;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .brand-title {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .brand-tagline {
        font-size: 1.1rem;
        color: #9fb3c8;
        font-weight: 300;
        margin-bottom: 50px;
    }

    /* Input Overrides: Minimalist Underline Style */
    div.stTextInput > div > div > input {
        background-color: transparent !important;
        color: white !important;
        border: none !important;
        border-bottom: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 0px !important;
        height: 45px;
        font-size: 1.1rem;
        padding-left: 0px !important;
    }
    div.stTextInput > label { color: #829ab1 !important; }

    /* Login Button Styling */
    div.stButton > button {
        background: #ffffff !important;
        color: #102a43 !important;
        border-radius: 30px !important;
        height: 55px;
        width: 100%;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        margin-top: 35px;
        border: none;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    div.stButton > button:hover {
        background: #d9e2ec !important;
        transform: scale(1.03);
    }

    /* Itinerary Result Styling */
    .itinerary-card {
        background: white;
        color: #243b53;
        padding: 45px;
        border-radius: 25px;
        margin-top: 40px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
        border-left: 12px solid #334e68;
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_ai_travel_system(query):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Role: Multi-Agent Travel Planner for: {query}.
        Organize response as:
        1. 🧭 Route Architect: Best scenic path & stopovers.
        2. 📅 Master Planner: Detailed day-wise itinerary.
        3. 🥘 Culture Expert: Top 3 local foods & budget in INR.
        Language: English & Telugu Mix. Professional Markdown.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "🚨 Connection Error: Ensure GOOGLE_API_KEY is in st.secrets."

# --- 4. SESSION MANAGEMENT ---
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = False
if 'plan_data' not in st.session_state:
    st.session_state.plan_data = None

# --- 5. THE LOGIN PAGE (THE LOOK YOU WANTED) ---
if not st.session_state.auth_state:
    # Encapsulating HTML for the split layout
    st.markdown(f"""
        <div class="travel-canvas">
            <div class="left-hero">
                <div class="quote-style">
                    "Travel is the only thing<br>you buy that makes<br>you richer"
                </div>
            </div>
            <div class="right-auth">
    """, unsafe_allow_html=True)
    
    # Real Streamlit Input Components (placed in the right panel via logic)
    st.markdown('<div class="brand-title">YatriMate AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tagline">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
    
    user_id = st.text_input("Traveler Email", placeholder="veera@traveler.com")
    user_pk = st.text_input("Access Secret", type="password", placeholder="••••••••")
    
    if st.button("ENTER THE HORIZON 🚀"):
        if user_id == "veera@traveler.com" and user_pk == "buddy_password_2026":
            st.session_state.auth_state = True
            st.rerun()
        else:
            st.error("Access Denied. Please verify credentials.")
            
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- 6. THE TRAVELER DASHBOARD ---
else:
    with st.sidebar:
        st.markdown("### 🧭 YatriMate AI")
        st.info("Status: Authenticated")
        if st.button("Logout 🚪"):
            st.session_state.auth_state = False
            st.session_state.plan_data = None
            st.rerun()

    st.markdown("<h2 style='text-align:center; color:#102a43; margin-top:40px;'>Curate Your Next Journey</h2>", unsafe_allow_html=True)
    
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        query = st.text_input("", placeholder="e.g., Hyderabad to Varanasi via Nagpur", label_visibility="collapsed")
        if st.button("PLAN MY ADVENTURE 🌍"):
            if query:
                with st.status("🔮 Coordinating AI Agents...", expanded=True) as s:
                    st.write("🕵️ Route Architect is calculating paths...")
                    time.sleep(1)
                    res = run_ai_travel_system(query)
                    st.session_state.plan_data = res
                    s.update(label="Full Plan Ready!", state="complete")

    if st.session_state.plan_data:
        st.markdown(f'<div class="itinerary-card">{st.session_state.plan_data}</div>', unsafe_allow_html=True)
        if st.button("🔄 New Search"):
            st.session_state.plan_data = None
            st.rerun()

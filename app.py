import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CORE SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI DESIGN SYSTEM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Moving Luxury Background */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1e1b4b 0%, #0f172a 50%, #020617 100%);
        background-attachment: fixed;
    }

    /* Floating Glass Card */
    .hero-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(35px);
        -webkit-backdrop-filter: blur(35px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 60px 45px;
        border-radius: 50px;
        box-shadow: 0 50px 100px rgba(0,0,0,0.7);
        text-align: center;
        max-width: 620px;
        margin: auto;
        margin-top: 30px;
    }

    /* 3D Robot Animation */
    .robot-buddy {
        width: 190px;
        filter: drop-shadow(0 0 35px rgba(59, 130, 246, 0.6));
        animation: floatRobot 5s ease-in-out infinite;
    }
    @keyframes floatRobot {
        0%, 100% { transform: translateY(0px) rotate(-1deg); }
        50% { transform: translateY(-30px) rotate(1deg); }
    }

    /* Branding & Quote Styling */
    .brand-title {
        background: linear-gradient(120deg, #ffffff, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.8rem;
        margin-bottom: 5px;
        letter-spacing: -2px;
    }
    .brand-quote {
        color: #94a3b8;
        font-size: 1.25rem;
        font-weight: 300;
        margin-bottom: 40px;
        font-style: italic;
        letter-spacing: 1px;
    }

    /* Modern Minimalist Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 60px;
        font-size: 1.15rem;
        padding-left: 25px;
    }

    /* Luxury Action Button */
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
        color: white !important;
        border-radius: 20px !important;
        height: 65px;
        width: 100%;
        font-weight: 700;
        font-size: 1.3rem;
        border: none;
        box-shadow: 0 15px 40px rgba(37, 99, 235, 0.4);
        transition: 0.5s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 60px rgba(37, 99, 235, 0.6);
    }

    /* Clean Itinerary Result Paper */
    .itinerary-paper {
        background: #ffffff;
        color: #0f172a;
        padding: 45px;
        border-radius: 40px;
        border-left: 18px solid #2563eb;
        margin-top: 40px;
        line-height: 1.8;
        box-shadow: 0 30px 70px rgba(0,0,0,0.5);
    }

    /* Hide Streamlit elements for clean look */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_ai_agents(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel Intelligence for: {query}.
        Structure the response with 3 Specialized Agents:
        1. 🗺️ Agent 'Route Architect': Suggest 2-3 middle stopovers for a scenic route.
        2. 🗓️ Agent 'Itinerary Planner': Provide a detailed, logical day-wise schedule.
        3. 🥘 Agent 'Culture Expert': Suggest 3 local must-try foods and a budget estimate in INR.
        Language: {lang}. Format: High-quality Markdown with icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 API Key missing or invalid. Error: {str(e)}"

# --- 4. STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 5. AUTHENTICATION UI (The Modern Traveler Experience) ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([0.5, 2, 0.5])
    with col2:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        # Visual 3D Asset
        st.markdown('<img src="https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png" class="robot-buddy">', unsafe_allow_html=True)
        
        st.markdown('<div class="brand-title">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-quote">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)

        mode = option_menu(None, ["Explorer Login", "Join the Club"], 
            icons=['shield-lock', 'person-plus-fill'], orientation="horizontal",
            styles={
                "container": {"background-color": "transparent", "padding": "0"},
                "nav-link": {"color": "#94a3b8", "font-size": "15px", "font-weight": "600"},
                "nav-link-selected": {"background-color": "#2563eb", "color": "white", "border-radius": "15px"}
            })

        if mode == "Explorer Login":
            st.text_input("Traveler Email", placeholder="veera@traveler.com", key="email_field")
            st.text_input("Secret Access Key", type="password", placeholder="••••••••", key="pwd_field")
            if st.button("Access Dashboard 🚀"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            st.text_input("Full Name")
            st.text_input("Email ID")
            st.text_input("Set Access Key", type="password")
            if st.button("Start My Adventure ✨"):
                st.success("Registration Successful! Please Sign In.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MAIN DASHBOARD ---
else:
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 style="color:white;">YatriMate AI</h2>', unsafe_allow_html=True)
        st.image("https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png", width=120)
        st.write("---")
        if st.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.itinerary_data = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white; font-size:3rem;'>Discover Your Next Horizon</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8; font-size:1.1rem;'>The Buddy AI Agents are ready to map your trip.</p>", unsafe_allow_html=True)

    # Search Logic
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        query = st.text_input("", placeholder="e.g., Hyderabad to Varanasi via Nagpur", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if query:
                with st.status("🔮 Coordinating AI Intelligence...", expanded=True) as status:
                    st.write("🕵️ Route Architect is calculating paths...")
                    time.sleep(1)
                    st.write("🗓️ Itinerary Planner is mapping the days...")
                    res = run_ai_agents(query, "English & Telugu Mix")
                    st.session_state.itinerary_data = res
                    status.update(label="Full Curation Complete!", state="complete")

    # Result Section
    if st.session_state.itinerary_data:
        st.markdown(f'<div class="itinerary-paper">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)
        if st.button("🔄 Plan New Journey"):
            st.session_state.itinerary_data = None
            st.rerun()
    else:
        # Trending Horizons Grid
        st.write("---")
        st.markdown("<h3 style='text-align:center; color:white;'>Trending Horizons</h3>", unsafe_allow_html=True)
        t_cols = st.columns(4)
        horizons = [
            ("Varanasi", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"),
            ("Ladakh", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?w=400"),
            ("Andaman", "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"),
            ("Goa", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400")
        ]
        for i, (name, img) in enumerate(horizons):
            with t_cols[i]:
                st.image(img, use_container_width=True, caption=name)

    st.markdown("<br><p style='text-align:center; color:#475569;'>© 2026 YatriMate AI | Your AI Compass for Every Horizon</p>", unsafe_allow_html=True)

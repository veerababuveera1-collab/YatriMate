import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. CORE SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM MODERN TRAVELER UI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Modern Dark Canvas Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
        background-attachment: fixed;
    }

    /* Glassmorphism Auth Card */
    .hero-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px 40px;
        border-radius: 40px;
        box-shadow: 0 50px 100px rgba(0,0,0,0.8);
        text-align: center;
        max-width: 600px;
        margin: auto;
        margin-top: 30px;
    }

    /* 3D Robot Buddy Visual Animation */
    .robot-buddy {
        width: 180px;
        filter: drop-shadow(0 0 30px rgba(59, 130, 246, 0.6));
        animation: floatRobot 5s ease-in-out infinite;
    }
    @keyframes floatRobot {
        0%, 100% { transform: translateY(0px) rotate(-2deg); }
        50% { transform: translateY(-25px) rotate(2deg); }
    }

    /* Branding & Quotes */
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
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 35px;
        font-style: italic;
    }

    /* Modern Glass Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 55px;
        font-size: 1.1rem;
        padding-left: 20px;
    }
    div.stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }

    /* Action Buttons (Traveler Blue) */
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb, #6366f1) !important;
        color: white !important;
        border-radius: 18px !important;
        height: 60px;
        width: 100%;
        font-weight: 700;
        font-size: 1.2rem;
        border: none;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.4);
        transition: 0.4s ease;
        text-transform: capitalize;
    }
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(37, 99, 235, 0.6);
    }

    /* White Itinerary Result Card */
    .itinerary-card {
        background: #ffffff;
        color: #0f172a;
        padding: 40px;
        border-radius: 35px;
        border-left: 15px solid #2563eb;
        margin-top: 35px;
        line-height: 1.7;
        box-shadow: 0 30px 60px rgba(0,0,0,0.4);
    }

    /* Customizing Option Menu */
    .nav-link { color: #94a3b8 !important; font-weight: 600 !important; }
    .nav-link-selected { background-color: #2563eb !important; color: white !important; border-radius: 12px !important; }

    /* Hide default Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_yatri_agents(query, lang):
    try:
        # Fetching API Key from Streamlit Secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for the trip: {query}.
        Provide the response by coordinating between these 3 Agents:
        1. 🗺️ Agent 'Route Architect': Suggest 2-3 mandatory middle stopovers for a scenic/logical route.
        2. 🗓️ Agent 'Itinerary Planner': Provide a detailed day-wise adventure schedule.
        3. 🥘 Agent 'Budget & Food Expert': Estimate total cost in INR and suggest 3 must-try local foods.
        Language: {lang}. Use Markdown with professional icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 API Connection Issue: Please check your configuration. {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'adventure_plan' not in st.session_state:
    st.session_state.adventure_plan = None

# --- 5. AUTHENTICATION UI (The Modern Login) ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([0.5, 2, 0.5])
    with col2:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        # 3D Robot Asset
        st.markdown('<img src="https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png" class="robot-buddy">', unsafe_allow_html=True)
        
        st.markdown('<div class="brand-title">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-quote">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)

        mode = option_menu(None, ["Sign In", "New Traveler"], 
            icons=['fingerprint', 'person-plus-fill'], orientation="horizontal",
            styles={
                "container": {"background-color": "transparent", "padding": "0"},
                "nav-link": {"font-size": "15px", "margin":"5px"},
            })

        if mode == "Sign In":
            st.text_input("Traveler ID (Email)", placeholder="veera@traveler.com", key="login_id")
            st.text_input("Access Key (Password)", type="password", placeholder="••••••••", key="login_key")
            if st.button("Unlock Dashboard 🌍"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            st.text_input("Full Name", placeholder="Your Name")
            st.text_input("Email ID", placeholder="buddy@example.com")
            st.text_input("Set Access Key", type="password", placeholder="••••••••")
            if st.button("Begin Journey ✨"):
                st.success("Account Created! Use 'Sign In' to enter.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. TRAVELER DASHBOARD ---
else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown('<h2 style="color:white;">YatriMate AI</h2>', unsafe_allow_html=True)
        st.image("https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png", width=110)
        st.write("---")
        if st.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.adventure_plan = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white;'>Where does your curiosity lead today?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8; font-size:1.1rem;'>Buddy AI Agents are standing by to map your adventure.</p>", unsafe_allow_html=True)

    # Search Logic
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        query = st.text_input("", placeholder="e.g., Hyderabad to Varanasi via Nagpur", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if query:
                with st.status("🤖 Buddy is coordinating with Agents...", expanded=True) as status:
                    st.write("🕵️ Route Architect is calculating the best stops...")
                    time.sleep(1)
                    st.write("🗓️ Itinerary Planner is mapping the days...")
                    res = run_yatri_agents(query, "English & Telugu Mix")
                    st.session_state.adventure_plan = res
                    status.update(label="Adventure Plan Complete!", state="complete")

    # Result Section
    if st.session_state.adventure_plan:
        st.markdown(f'<div class="itinerary-card">{st.session_state.adventure_plan}</div>', unsafe_allow_html=True)
        if st.button("🔄 Plan Another Horizon"):
            st.session_state.adventure_plan = None
            st.rerun()
    else:
        # Visual Trending Grid
        st.write("---")
        st.markdown("<h3 style='text-align:center; color:white;'>Trending Horizons</h3>", unsafe_allow_html=True)
        grid = st.columns(4)
        destinations = [
            ("Varanasi", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"),
            ("Leh Ladakh", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?w=400"),
            ("Andaman", "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"),
            ("Goa", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400")
        ]
        for i, (name, img) in enumerate(destinations):
            with grid[i]:
                st.image(img, use_container_width=True, caption=name)

    # Footer
    st.markdown("<br><p style='text-align:center; color:#475569;'>© 2026 YatriMate AI | Your AI Compass for Every Horizon</p>", unsafe_allow_html=True)

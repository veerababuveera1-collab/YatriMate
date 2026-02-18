import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Travel Buddy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI & ANIMATIONS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    * { font-family: 'Outfit', sans-serif; }

    /* Premium Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #1e3a8a, #020617);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Auth Card */
    .auth-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 40px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.5);
        text-align: center;
        max-width: 500px;
        margin: auto;
    }

    /* 3D Robot Buddy Animation */
    .robot-buddy {
        width: 180px;
        filter: drop-shadow(0 0 25px rgba(59, 130, 246, 0.7));
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-20px) scale(1.05); }
    }

    /* Input & Button Styling */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 50px;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 55px;
        width: 100%;
        font-weight: 800;
        border: none;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.5);
    }

    /* Result Box (Itinerary) */
    .report-box {
        background: white; color: #111827; padding: 40px; 
        border-radius: 30px; border-left: 12px solid #3b82f6;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_ai_travel_system(query, lang):
    try:
        # Get Key from Streamlit Secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Structure your response using 3 specialized Agents:
        1. 🕵️ Agent 'Route Architect': Suggest 2-3 middle stopovers.
        2. 📅 Agent 'Itinerary Planner': Provide a detailed day-wise schedule.
        3. 💰 Agent 'Budget & Food Expert': Estimate cost in INR and 3 local foods.
        Language: {lang}. Use Markdown with icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# --- 5. AUTHENTICATION UI (Sign In / Sign Up) ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<img src="https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png" class="robot-buddy">', unsafe_allow_html=True)
        st.markdown("<h2 style='color:white;'>Welcome to Sign Up Buddy!</h2>", unsafe_allow_html=True)
        
        mode = option_menu(None, ["Sign In", "Sign Up"], 
            icons=['fingerprint', 'person-plus'], orientation="horizontal",
            styles={"container": {"background-color": "transparent"}, "nav-link-selected": {"background-color": "#3b82f6"}})

        if mode == "Sign In":
            st.text_input("Email", placeholder="Enter your email", key="l_email")
            st.text_input("Password", type="password", placeholder="••••••••", key="l_pwd")
            if st.button("LOG IN 🚀"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            st.text_input("Full Name", placeholder="Your Name")
            st.text_input("Email Address", placeholder="buddy@example.com")
            st.text_input("Create Password", type="password")
            if st.button("CREATE ACCOUNT ✨"):
                st.success("Account Created! Please Sign In.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MAIN DASHBOARD ---
else:
    # Sidebar
    st.sidebar.markdown('<img src="https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png" width="100">', unsafe_allow_html=True)
    if st.sidebar.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.session_state.itinerary = None
        st.rerun()

    st.markdown("<h1 style='text-align:center; color:white;'>🚩 YatriMate AI Buddy Dashboard</h1>", unsafe_allow_html=True)
    
    # Input Logic
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        user_query = st.text_input("", placeholder="Where are we heading today? (e.g. Hyd to Varanasi)", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if user_query:
                with st.status("🤖 Buddy is coordinating with Agents...", expanded=True) as s:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    st.write("📅 Itinerary Planner is mapping days...")
                    res = run_ai_travel_system(user_query, "Telugu & English Mix")
                    st.session_state.itinerary = res
                    s.update(label="Full Plan Ready!", state="complete")

    # Show Results
    if st.session_state.itinerary:
        st.markdown(f'<div class="report-box">{st.session_state.itinerary}</div>', unsafe_allow_html=True)
        if st.button("🔄 Plan New Journey"):
            st.session_state.itinerary = None
            st.rerun()
    else:
        # Trending Section
        st.write("---")
        st.markdown("<h3 style='text-align:center; color:white;'>🌍 Trending Now</h3>", unsafe_allow_html=True)
        t_cols = st.columns(4)
        dests = [
            ("Varanasi", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"),
            ("Andaman", "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"),
            ("Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"),
            ("Bali", "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400")
        ]
        for i, (name, img) in enumerate(dests):
            with t_cols[i]:
                st.image(img, use_container_width=True, caption=name)

    # Footer
    st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>© 2026 YatriMate AI | Multi-Agent Travel Intelligence</p>", unsafe_allow_html=True)

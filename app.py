import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Premium Buddy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI & TRAVELER LOOK CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    * { font-family: 'Outfit', sans-serif; }

    /* Premium Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e3a8a, #1e1b4b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Auth Card */
    .auth-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 50px;
        border-radius: 50px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.6);
        text-align: center;
        max-width: 550px;
        margin: auto;
        margin-top: 20px;
    }

    /* 3D Robot Buddy Animation */
    .robot-buddy {
        width: 200px;
        filter: drop-shadow(0 0 25px rgba(59, 130, 246, 0.7));
        animation: floatRobot 4s ease-in-out infinite;
        margin-bottom: 10px;
    }
    @keyframes floatRobot {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-25px) rotate(3deg); }
    }

    /* Headlines & Neon Text */
    h2 { 
        background: linear-gradient(90deg, #ffffff, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.5rem; 
    }
    p { color: #94a3b8 !important; font-size: 1.1rem; }

    /* Modern Inputs */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 55px;
        font-size: 1.1rem;
    }

    /* Premium Neon Button */
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
        color: white !important;
        border-radius: 18px !important;
        height: 60px;
        width: 100%;
        font-weight: 800;
        font-size: 1.2rem;
        border: none;
        transition: 0.4s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.5);
    }

    /* White Result Box */
    .itinerary-box {
        background: #ffffff;
        color: #111827;
        padding: 40px;
        border-radius: 35px;
        border-left: 15px solid #3b82f6;
        margin-top: 30px;
        text-align: left;
    }

    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_ai_travel_buddy(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Provide the response using these 3 specialized Agents:
        1. 🕵️ Agent 'Route Architect': Suggest 2-3 mandatory middle stopovers.
        2. 📅 Agent 'Itinerary Planner': Create a logical day-wise schedule.
        3. 💰 Agent 'Budget & Food Expert': Estimate cost in INR and suggest 3 local dishes.
        Language: {lang}. Format: Clean Markdown with icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: Please check your API Key. Details: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'plan' not in st.session_state:
    st.session_state.plan = None

# --- 5. AUTHENTICATION UI (Login / Sign Up) ---
if not st.session_state.logged_in:
    _, center_col, _ = st.columns([0.5, 2, 0.5])
    with center_col:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        # Fixed High-Quality 3D Buddy Image
        st.markdown('<img src="https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png" class="robot-buddy">', unsafe_allow_html=True)
        
        st.markdown("<h2>Welcome Buddy!</h2>", unsafe_allow_html=True)
        st.markdown("<p>Plan your luxury journey with AI</p>", unsafe_allow_html=True)

        mode = option_menu(None, ["Sign In", "Sign Up"], 
            icons=['fingerprint', 'person-plus'], orientation="horizontal",
            styles={
                "container": {"background-color": "transparent"},
                "nav-link-selected": {"background-color": "#3b82f6", "border-radius": "15px"}
            })

        if mode == "Sign In":
            st.text_input("Email", placeholder="buddy@example.com", key="login_email")
            st.text_input("Password", type="password", placeholder="••••••••", key="login_pwd")
            if st.button("Unlock Dashboard 🚀"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            st.text_input("Full Name", placeholder="Your Name")
            st.text_input("Email Address")
            st.text_input("Set Password", type="password")
            if st.button("Start My Journey ✨"):
                st.success("Account Ready! Now Sign In.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MAIN DASHBOARD ---
else:
    # Sidebar
    with st.sidebar:
        st.markdown('<img src="https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png" width="120">', unsafe_allow_html=True)
        st.write("---")
        if st.button("Sign Out 🚪"):
            st.session_state.logged_in = False
            st.session_state.plan = None
            st.rerun()

    st.markdown("<h1 style='text-align:center; color:white;'>🌍 YatriMate AI Buddy Dashboard</h1>", unsafe_allow_html=True)
    
    # Input Area
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        u_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (e.g. Hyderabad to Mumbai via Pune)", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if u_query:
                with st.status("🤖 Buddy is coordinating with Agents...", expanded=True) as status:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    st.write("📅 Itinerary Planner is mapping days...")
                    res = run_ai_travel_buddy(u_query, "Telugu & English Mix")
                    st.session_state.plan = res
                    status.update(label="Full Plan Ready!", state="complete")

    # Display Result
    if st.session_state.plan:
        st.markdown(f'<div class="itinerary-box">{st.session_state.plan}</div>', unsafe_allow_html=True)
        if st.button("🔄 Start New Plan"):
            st.session_state.plan = None
            st.rerun()
    else:
        # Trending Section
        st.write("---")
        st.markdown("<h3 style='text-align:center; color:white;'>🌍 Trending Destinations</h3>", unsafe_allow_html=True)
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

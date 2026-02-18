import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Your Travel Buddy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THEME & PINTEREST-ENVATO STYLE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important;
    }

    /* Auth Card (Envato Style) */
    .auth-container {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(15px);
        padding: 50px;
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 60px rgba(0,0,0,0.6);
        text-align: center;
        max-width: 550px;
        margin: auto;
    }

    /* 3D Buddy Animation */
    .robot-buddy {
        width: 180px;
        filter: drop-shadow(0 0 15px rgba(59, 130, 246, 0.6));
        animation: float 4s ease-in-out infinite;
        margin-bottom: 10px;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    /* Text & Input Styling */
    h1, h2 { color: #ffffff !important; font-weight: 800; }
    p { color: #94a3b8 !important; }
    
    div.stTextInput > div > div > input {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid #334155 !important;
        height: 50px;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6, #1d4ed8) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 55px;
        width: 100%;
        font-weight: 700;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }

    /* Result Result Box */
    .itinerary-box {
        background: #ffffff;
        color: #1a1a1a;
        padding: 40px;
        border-radius: 30px;
        border-left: 12px solid #3b82f6;
        margin-top: 25px;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI AGENT ENGINE ---
def run_multi_agent_system(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Structure the output using these 3 specialized AI Agents:
        1. 🕵️ Agent 'Route Architect': Suggest 2-3 mandatory middle stopovers.
        2. 📅 Agent 'Itinerary Planner': Create a day-wise logical schedule.
        3. 💰 Agent 'Budget & Food Expert': Estimate cost in INR and 3 local foods.
        Language: {lang}. Use Markdown with icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# --- 5. AUTHENTICATION UI (LOGIN/REGISTER) ---
if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        # Professional 3D Robot Image
        st.markdown('<img src="https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png" class="robot-buddy">', unsafe_allow_html=True)
        st.markdown("<h2>Welcome to Sign Up Buddy!</h2>", unsafe_allow_html=True)
        
        mode = option_menu(None, ["Sign In", "Sign Up"], 
            icons=['lock', 'person-plus'], 
            menu_icon="cast", default_index=0, orientation="horizontal",
            styles={"container": {"background-color": "transparent"}, "nav-link-selected": {"background-color": "#3b82f6"}})

        if mode == "Sign In":
            email = st.text_input("Email", placeholder="buddy@example.com")
            pwd = st.text_input("Password", type="password")
            if st.button("SIGN IN"):
                if email and pwd:
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("Enter details")
        else:
            st.text_input("Full Name")
            st.text_input("Email")
            st.text_input("Create Password", type="password")
            if st.button("CREATE ACCOUNT"):
                st.success("Account Created! Please Sign In.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MAIN APPLICATION DASHBOARD ---
else:
    # Sidebar
    with st.sidebar:
        st.image("https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png", width=100)
        st.write("---")
        if st.button("Sign Out 🚪"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<h1 style='text-align:center;'>🚩 YatriMate AI Dashboard</h1>", unsafe_allow_html=True)
    
    # Search Section
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (e.g. Hyderabad to Varanasi)", label_visibility="collapsed")
        if st.button("ACTIVATE AI AGENTS 🚀"):
            if query:
                with st.status("🤖 Buddy is planning...", expanded=True) as status:
                    st.write("🕵️ Finding stopovers...")
                    time.sleep(1)
                    st.write("📅 Organizing schedule...")
                    res = run_multi_agent_system(query, "Telugu & English Mix")
                    st.session_state.itinerary = res
                    status.update(label="Planning Complete!", state="complete")

    # Display Result
    if st.session_state.itinerary:
        st.markdown(f'<div class="itinerary-box">{st.session_state.itinerary}</div>', unsafe_allow_html=True)
        if st.button("🔄 New Trip"):
            st.session_state.itinerary = None
            st.rerun()
    else:
        # Trending Section
        st.write("---")
        st.markdown("<h3 style='text-align:center;'>🌍 Trending Now</h3>", unsafe_allow_html=True)
        d_cols = st.columns(4)
        dests = [
            ("Varanasi", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"),
            ("Andaman", "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"),
            ("Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"),
            ("Bali", "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400")
        ]
        for i, (name, img) in enumerate(dests):
            with d_cols[i]:
                st.image(img, use_container_width=True, caption=name)

    # Footer
    st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.8rem;'>© 2026 YatriMate AI | Multi-Agent Travel Intelligence</p>", unsafe_allow_html=True)

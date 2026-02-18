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

# --- 2. ENVATO DARK BLUE THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }

    /* Full Page Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    }

    /* Auth & Content Container */
    .main-card {
        background: rgba(17, 24, 39, 0.8);
        backdrop-filter: blur(10px);
        padding: 50px;
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        text-align: center;
        max-width: 600px;
        margin: auto;
    }

    /* 3D Robot Animation */
    .robot-buddy {
        width: 150px;
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    /* Typography */
    h1, h2, h3 { color: #ffffff !important; font-weight: 800; }
    p { color: #94a3b8 !important; }

    /* Input & Button Styling */
    div.stTextInput > div > div > input {
        background-color: #1f2937 !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid #3b82f6 !important;
        height: 50px;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 55px;
        width: 100%;
        font-weight: 800;
        border: none;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
    }

    /* Results Box */
    .itinerary-box {
        background: #ffffff;
        color: #1a1a1a;
        padding: 40px;
        border-radius: 30px;
        border-left: 15px solid #2563eb;
        text-align: left;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT AI ENGINE ---
def run_travel_agent_system(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Structure the response using these 3 specialized AI Agents:
        1. 🕵️ Agent 'Route Architect': Identify 2-3 mandatory 'Middle Destination' stops between the source and final destination.
        2. 📅 Agent 'Itinerary Planner': Create a detailed day-wise schedule.
        3. 💰 Agent 'Budget & Food Expert': Estimate cost in INR and suggest 3 local dishes.
        Language: {lang}. Format: Clean Markdown with icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- 4. AUTHENTICATION LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'plan_data' not in st.session_state:
    st.session_state.plan_data = None

if not st.session_state.logged_in:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.image("https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png", width=180)
        st.markdown("<h2>Welcome to Sign Up Buddy!</h2>", unsafe_allow_html=True)
        
        auth_choice = option_menu(None, ["Sign In", "Sign Up"], 
            icons=['key', 'person-plus'], orientation="horizontal",
            styles={"container": {"background-color": "transparent"}, "nav-link-selected": {"background-color": "#2563eb"}})

        if auth_choice == "Sign In":
            email = st.text_input("Email Address", placeholder="buddy@example.com")
            pwd = st.text_input("Password", type="password")
            if st.button("SIGN IN"):
                st.session_state.logged_in = True
                st.rerun()
        else:
            st.text_input("Full Name")
            st.text_input("Email Address")
            st.text_input("Create Password", type="password")
            if st.button("SIGN UP"):
                st.success("Account Ready! Please Sign In.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD ---
else:
    # Logout in Sidebar
    st.sidebar.image("https://cdn3d.iconscout.com/3d/premium/thumb/robot-saying-hello-4835150-4027063.png", width=100)
    if st.sidebar.button("Sign Out 🚪"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("<h1 style='text-align:center;'>🚩 YatriMate AI - Smart Planner</h1>", unsafe_allow_html=True)
    
    # Input Section
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        u_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (e.g. Hyd to Goa)", label_visibility="collapsed")
        if st.button("ACTIVATE AGENTS 🚀"):
            if u_query:
                with st.status("🤖 Buddy is planning your trip...", expanded=True) as s:
                    st.write("🕵️ Route Architect is finding hidden gems...")
                    time.sleep(1)
                    st.write("📅 Itinerary Planner is mapping days...")
                    res = run_travel_agent_system(u_query, "Telugu & English Mix")
                    st.session_state.plan_data = res
                    s.update(label="Plan Complete!", state="complete")

    # Display Result
    if st.session_state.plan_data:
        st.markdown(f'<div class="itinerary-box">{st.session_state.plan_data}</div>', unsafe_allow_html=True)
        if st.button("🔄 New Journey"):
            st.session_state.plan_data = None
            st.rerun()
    else:
        # Trending Row
        st.write("---")
        st.markdown("<h3 style='text-align:center;'>🌍 Trending Destinations</h3>", unsafe_allow_html=True)
        cols = st.columns(4)
        dests = [
            ("Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"),
            ("Varanasi", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"),
            ("Andaman", "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"),
            ("Bali", "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400")
        ]
        for i, (name, img) in enumerate(dests):
            with cols[i]:
                st.image(img, use_container_width=True, caption=name)

    # Footer
    st.markdown("<br><p style='text-align:center; color:#94a3b8;'>© 2026 YatriMate AI | Saidabad, Hyderabad</p>", unsafe_allow_html=True)

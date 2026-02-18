import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
import time

# --- 1. SYSTEM & UI CONFIGURATION ---
st.set_page_config(page_title="YatriMate AI - Multi-Agent Planner", page_icon="🤖", layout="wide")

# --- 2. CUSTOM CSS (PINTEREST & MODERN UI STYLE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    /* Background and Auth Card */
    .stApp { background-color: #f7f9fc; }
    .auth-card {
        background: white; padding: 40px; border-radius: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05); text-align: center;
        max-width: 450px; margin: auto; border: 1px solid #eee;
    }
    .robot-icon { width: 100px; margin-bottom: 20px; transition: 0.5s; }
    .robot-icon:hover { transform: translateY(-5px) rotate(5deg); }

    /* Itinerary Result Box */
    .report-box {
        background: white; color: #1a1a1a; padding: 40px; 
        border-radius: 25px; border-left: 10px solid #6C63FF;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 20px;
    }

    /* Buttons & Inputs */
    div.stButton > button {
        background: linear-gradient(90deg, #6C63FF, #4B45E5) !important;
        color: white !important; border-radius: 12px; height: 50px;
        width: 100%; font-weight: bold; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(108, 99, 255, 0.3); }
    
    /* Destination Cards */
    .dest-card {
        background: white; border-radius: 20px; overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08); transition: 0.4s; text-align: center;
    }
    .dest-card:hover { transform: translateY(-10px); }
    .dest-img { width: 100%; height: 160px; object-fit: cover; }
    .dest-label { padding: 10px; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MULTI-AGENT ENGINE LOGIC ---
def run_travel_agent_system(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Structure your response from these 3 AI Agents:
        1. 🕵️ Agent 'Route Architect': Suggest 2-3 middle stopovers between source and destination.
        2. 📅 Agent 'Itinerary Planner': Provide a day-wise logical schedule.
        3. 💰 Agent 'Budget & Food Expert': Estimate cost in INR and list 3 local foods.
        Language: {lang}. Format: Clean Markdown with icons.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: Please check your secrets. {str(e)}"

# --- 4. SESSION STATE FOR LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# --- 5. AUTHENTICATION UI (LOGIN/REGISTER) ---
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        # Pinterest Style Robot Image
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
        
        mode = option_menu(None, ["Login", "Register"], 
            icons=['person', 'person-plus'], 
            menu_icon="cast", default_index=0, orientation="horizontal",
            styles={"container": {"padding": "0!important", "background-color": "#f8f9fa"}})

        if mode == "Login":
            st.markdown("### Welcome Back!")
            email = st.text_input("Email", placeholder="yourname@gmail.com")
            password = st.text_input("Password", type="password")
            if st.button("Start Journey 🚀"):
                if email and password:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.warning("Please enter credentials.")
        else:
            st.markdown("### Create Account")
            st.text_input("Full Name")
            st.text_input("Email")
            st.text_input("Create Password", type="password")
            if st.button("Register Now ✨"):
                st.success("Account Created! Please Login.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MAIN APP DASHBOARD ---
else:
    # Sidebar Logout
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
        st.write("---")
        if st.button("Sign Out 🚪"):
            st.session_state.logged_in = False
            st.session_state.itinerary = None
            st.rerun()

    st.markdown("<h1 style='text-align: center; color: #333;'>🚩 YatriMate AI Planner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>మీ ప్రయాణాన్ని స్మార్ట్ ఏజెంట్లతో ప్లాన్ చేయండి</p>", unsafe_allow_html=True)

    # Search Bar
    sc1, sc2, sc3 = st.columns([1, 3, 1])
    with sc2:
        user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (e.g. Hyderabad to Varanasi via Nagpur)", label_visibility="collapsed")
        if st.button("Activate AI Agents 🚀", use_container_width=True):
            if user_query:
                with st.status("🤖 Coordinating Agents...", expanded=True) as status:
                    st.write("🕵️ Route Architect is mapping stops...")
                    time.sleep(1)
                    st.write("📅 Itinerary Planner is scheduling...")
                    time.sleep(1)
                    result = run_travel_agent_system(user_query, "Telugu & English Mix")
                    st.session_state.itinerary = result
                    status.update(label="Full Plan Ready!", state="complete")

    # Display Results
    if st.session_state.itinerary:
        st.markdown(f'<div class="report-box">{st.session_state.itinerary}</div>', unsafe_allow_html=True)
        if st.button("🔄 Plan Another Journey"):
            st.session_state.itinerary = None
            st.rerun()
    else:
        # Destination Cards GUI
        st.write("---")
        st.subheader("🌍 Trending Destinations")
        
        # Combined Destinations Row
        dests = [
            {"n": "Paris", "u": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"},
            {"n": "Varanasi", "u": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"},
            {"n": "Bali", "u": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400"},
            {"n": "Andaman", "u": "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"}
        ]
        
        cols = st.columns(4)
        for i, d in enumerate(dests):
            with cols[i]:
                st.markdown(f'''
                <div class="dest-card">
                    <img src="{d['u']}" class="dest-img">
                    <div class="dest-label">{d['n']}</div>
                </div>
                ''', unsafe_allow_html=True)

    # Footer
    st.markdown("<br><hr><p style='text-align: center; color: #aaa; font-size: 0.8rem;'>© 2026 YatriMate AI | Saidabad, Hyderabad | +91-6304001323</p>", unsafe_allow_html=True)

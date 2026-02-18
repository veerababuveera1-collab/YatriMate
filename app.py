import streamlit as st
import google.generativeai as genai
import time

# --- 1. CORE SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI | Your AI Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LUXURY UI ENGINE (Zero-Box Branding & Professional Image) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* New Professional High-Res Travel Background (Mountain Explorer) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.4)), 
                    url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Removing all default Streamlit block backgrounds for branding */
    [data-testid="stVerticalBlock"] > div:has(div.brand-h1) {
        background: transparent !important;
        padding: 0px !important;
        border: none !important;
    }

    /* Floating Branding - Clean & Modern (No Box) */
    .brand-h1 { 
        font-size: 5rem; 
        font-weight: 800; 
        letter-spacing: -3px; 
        margin-bottom: 0px;
        color: #ffffff;
        text-shadow: 0 10px 30px rgba(0,0,0,0.6);
        text-align: center;
    }
    .brand-tag { 
        font-size: 1.3rem; 
        opacity: 0.95; 
        font-weight: 300; 
        margin-top: -10px;
        margin-bottom: 40px;
        color: #ffffff;
        text-shadow: 0 4px 15px rgba(0,0,0,0.4);
        text-align: center;
    }

    /* Premium Glassmorphism Login Card */
    .login-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 55px 45px;
        border-radius: 40px;
        max-width: 480px;
        margin: auto;
        box-shadow: 0 50px 100px rgba(0,0,0,0.5);
        text-align: center;
        color: white;
    }

    /* Clean Inputs Styling */
    div.stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-radius: 18px !important;
        height: 60px;
        font-size: 1.1rem;
        border: none !important;
    }

    /* Primary Action Button */
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 18px !important;
        height: 60px;
        width: 100%;
        border: none;
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.4);
        transition: 0.4s;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 20px 45px rgba(37, 99, 235, 0.6); }

    /* Itinerary Output Container */
    .itinerary-container {
        background: white;
        color: #1a1a1a;
        padding: 45px;
        border-radius: 30px;
        border-left: 15px solid #2563eb;
        margin-top: 30px;
        box-shadow: 0 35px 70px rgba(0,0,0,0.5);
    }

    /* Destination Cards Styling */
    .img-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.4s ease;
        text-align: center;
        margin-bottom: 25px;
    }
    .img-card:hover { transform: translateY(-10px); border-color: #2563eb; }
    .dest-img { width: 100%; height: 180px; object-fit: cover; }
    .dest-label { padding: 12px; color: white; font-weight: bold; background: rgba(0,0,0,0.6); }

    header, footer {visibility: hidden;}
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
        Structure the response using these 3 specialized AI Agents:
        1. 🕵️ Agent 'Route Architect': Identify 2-3 mandatory stops and explain why.
        2. 📅 Agent 'Itinerary Planner': Create a detailed day-wise schedule.
        3. 🥘 Agent 'Budget & Food Expert': Give a budget in INR and list 3 local dishes.
        Output Language: {lang}.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# --- 4. SESSION MANAGEMENT ---
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = False
if 'itinerary_result' not in st.session_state:
    st.session_state.itinerary_result = None

# --- 5. INTERFACE (LOGIN OR DASHBOARD) ---
if not st.session_state.auth_status:
    _, mid_col, _ = st.columns([1, 2, 1])
    
    with mid_col:
        # BRANDING (Floating Text)
        st.markdown('<div class="brand-h1">YatriMate AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-tag">"Your AI Compass for Every Horizon"</div>', unsafe_allow_html=True)
        
        # LOGIN SECTION
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        user_in = st.text_input("Username", placeholder="veera@traveler.com", label_visibility="collapsed")
        pass_in = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        if st.button("SIGN IN 🚀"):
            if user_in == "veera@traveler.com" and pass_in == "buddy_password_2026":
                st.session_state.auth_status = True
                st.rerun()
            else:
                st.error("Invalid Login Details")

        st.markdown('<div style="margin: 25px 0; opacity: 0.5;">━━━━ or ━━━━</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.button("Google 🌐", use_container_width=True)
        with c2: st.button("Apple 🍎", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- AUTHENTICATED DASHBOARD ---
    st.markdown('<div class="brand-h1">YatriMate AI</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:white; text-align:center; margin-bottom:40px;">Smart Multi-Agent Intelligence for Journeys</p>', unsafe_allow_html=True)

    c_search, _ = st.columns([2, 1])
    with c_search:
        query = st.text_input("", placeholder="Enter Route (e.g., Hyderabad to Varanasi)...", label_visibility="collapsed")
        if st.button("Activate Agents 🚀"):
            if query:
                with st.status("🤖 AI Agents Coordinating...", expanded=True) as status:
                    result = run_travel_agent_system(query, "Telugu & English Mix")
                    st.session_state.itinerary_result = result
                    status.update(label="Planning Complete!", state="complete")
                    st.rerun()

    if st.session_state.itinerary_result:
        st.markdown(f'<div class="itinerary-container">{st.session_state.itinerary_result}</div>', unsafe_allow_html=True)
        if st.button("🔄 Plan Another Trip"):
            st.session_state.itinerary_result = None
            st.rerun()
    else:
        # Display Inspiration Cards
        st.markdown("<h3 style='color: white;'>🌍 International Getaways</h3>", unsafe_allow_html=True)
        intl_dests = [
            {"name": "Paris", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"},
            {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400"},
            {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400"},
            {"name": "Switzerland", "url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=400"}
        ]
        cols = st.columns(4)
        for i, d in enumerate(intl_dests):
            with cols[i]:
                st.markdown(f'<div class="img-card"><img src="{d["url"]}" class="dest-img"><div class="dest-label">{d["name"]}</div></div>', unsafe_allow_html=True)

    # Logout option in Sidebar
    with st.sidebar:
        st.title("🧭 YatriMate AI")
        if st.button("Logout 🚪"):
            st.session_state.auth_status = False
            st.rerun()

# --- 6. FOOTER ---
st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 30px; margin-top: 60px; text-align: center; color: white;">
        <p>© 2026 YatriMate AI | Multi-Agent Travel Intelligence</p>
    </div>
""", unsafe_allow_html=True)

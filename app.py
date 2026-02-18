import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Login",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 2. PREMIUM GUI STYLING (Global & Login Specific) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)), 
                    url("https://images.unsplash.com/photo-1503220317375-aaad61436b1b?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Login Card Styling */
    .login-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        max-width: 450px;
        margin: auto;
        text-align: center;
    }

    .hero-title {
        color: white !important; text-align: center; font-size: 3.5rem !important; 
        font-weight: 900; text-shadow: 0 10px 25px rgba(0,0,0,0.8); margin-bottom: 0px;
    }
    
    .sub-title {
        color: #FF9933 !important; text-align: center; font-size: 1.2rem; 
        font-weight: bold; margin-bottom: 30px;
    }

    /* Input Fields Styling */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Existing Page Elements */
    .img-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px; overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.4s ease; text-align: center;
        margin-bottom: 25px;
    }
    .img-card:hover {
        transform: translateY(-10px);
        border-color: #FF9933;
        box-shadow: 0 20px 40px rgba(255, 153, 51, 0.3);
    }
    .dest-img { width: 100%; height: 180px; object-fit: cover; }
    .dest-label { padding: 12px; color: white; font-weight: bold; background: rgba(0,0,0,0.6); }

    .itinerary-box {
        background: white; color: #1a1a1a; padding: 45px; 
        border-radius: 30px; border-left: 15px solid #FF9933;
        box-shadow: 0 30px 60px rgba(0,0,0,0.6); margin-top: 30px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important; border-radius: 12px !important;
        height: 50px; font-weight: bold; font-size: 1.1rem; border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE LOGIC ---
def login_page():
    st.markdown('<h1 class="hero-title">🚩 YatriMate</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Secure Agent Login</p>', unsafe_allow_html=True)
    
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        with st.form("Login Form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Engine 🚀")
            
            if submit:
                # Replace with your desired credentials
                if username == "admin" and password == "yatri123":
                    st.session_state.logged_in = True
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("Invalid Credentials. Please try again.")

# --- 4. MULTI-AGENT ENGINE LOGIC ---
def run_travel_agent_system(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Structure the response using these 3 specialized AI Agents:
        1. 🕵️ Agent 'Route Architect': Identify 2-3 mandatory stops.
        2. 📅 Agent 'Itinerary Planner': Create a detailed schedule.
        3. 💰 Agent 'Budget & Food Expert': Give estimate in INR and 3 local dishes.
        Output Language: {lang}.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# --- 5. MAIN APP (ONLY VISIBLE IF LOGGED IN) ---
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar Logout Button
    with st.sidebar:
        st.markdown("### User Profile")
        st.write("Logged in as: **Admin**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # --- HEADER & INPUT ---
    st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Smart Multi-Agent Intelligence for Global & Local Journeys</p>', unsafe_allow_html=True)

    if 'itinerary' not in st.session_state:
        st.session_state.itinerary = None

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        query = st.text_input("", placeholder="Enter Route (e.g., Hyderabad to Varanasi via Nagpur)...", label_visibility="collapsed")
        if st.button("Activate Agents 🚀"):
            if query:
                with st.status("🤖 AI Agents Coordinating...", expanded=True) as status:
                    result = run_travel_agent_system(query, "Telugu & English Mix")
                    st.session_state.itinerary = result
                    status.update(label="Planning Complete!", state="complete")
                    st.rerun()

    # --- RESULTS & CARDS ---
    if st.session_state.itinerary:
        st.markdown(f'<div class="itinerary-box">{st.session_state.itinerary}</div>', unsafe_allow_html=True)
        if st.button("🔄 Plan Another Trip"):
            st.session_state.itinerary = None
            st.rerun()
    else:
        # ROW 1: INTERNATIONAL
        st.markdown("<h3 style='color: white; margin-top: 20px;'>🌍 International Getaways</h3>", unsafe_allow_html=True)
        intl_dests = [
            {"name": "Paris, France", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"},
            {"name": "Dubai, UAE", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400"},
            {"name": "Bali, Indonesia", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400"},
            {"name": "Switzerland", "url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=400"}
        ]
        cols1 = st.columns(4)
        for i, d in enumerate(intl_dests):
            with cols1[i]:
                st.markdown(f'<div class="img-card"><img src="{d["url"]}" class="dest-img"><div class="dest-label">{d["name"]}</div></div>', unsafe_allow_html=True)

        # ROW 2: LOCAL
        st.markdown("<h3 style='color: white; margin-top: 20px;'>🏞️ Local Treasures</h3>", unsafe_allow_html=True)
        local_dests = [
            {"name": "Kerala Backwaters", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400"},
            {"name": "Varanasi Ghats", "url": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"},
            {"name": "Andaman Islands", "url": "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"},
            {"name": "Goa Beaches", "url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400"}
        ]
        cols2 = st.columns(4)
        for i, d in enumerate(local_dests):
            with cols2[i]:
                st.markdown(f'<div class="img-card"><img src="{d["url"]}" class="dest-img"><div class="dest-label">{d["name"]}</div></div>', unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 50px; border-radius: 30px; margin-top: 80px; border-top: 1px solid #FF9933;">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px;">
                <div style="flex: 2; min-width: 300px;">
                    <h2 style="color:#FF9933;">🚩 YatriMate AI</h2>
                    <p style="color:white; opacity: 0.8;">మీ ప్రయాణాన్ని పర్ఫెక్ట్‌గా ప్లాన్ చేసే మల్టీ-ఏజెంట్ AI సిస్టమ్.</p>
                </div>
                <div style="flex: 1; min-width: 250px; color:white;">
                    <h4>📍 Reach Us</h4>
                    <p>Saidabad Main Road, Hyderabad, 500059<br>
                    <b>Mobile:</b> +91-6304001323</p>
                </div>
            </div>
            <p style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 40px;'>© 2026 YatriMate AI</p>
        </div>
    """, unsafe_allow_html=True)

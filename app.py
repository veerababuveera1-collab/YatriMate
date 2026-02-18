import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Premium Travel Planner",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE CINEMATIC UI STYLING (Cleaned Version) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        /* High-Definition Cinematic Beach Sunset Background */
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)), 
                    url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2073");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 4rem !important;
        font-weight: 900;
        margin-bottom: 5px;
        letter-spacing: -2px;
        text-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.4rem;
        margin-bottom: 45px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Modern Glassmorphism Cards */
    .dest-card {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 25px;
        overflow: hidden;
        border: 1px solid rgba(255, 153, 51, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 290px;
        display: flex;
        flex-direction: column;
        margin-bottom: 30px;
    }
    .dest-card:hover {
        transform: translateY(-15px);
        border-color: #FF9933;
        box-shadow: 0 25px 50px rgba(255, 153, 51, 0.3);
    }
    .img-container {
        width: 100%;
        height: 200px;
    }
    .dest-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .dest-label {
        padding: 18px;
        color: white;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #000, #1a1a1a);
        font-size: 1.1rem;
        letter-spacing: 1px;
    }

    /* Premium Button Style */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933 0%, #FF5500 100%) !important;
        color: white !important;
        width: 100%;
        border-radius: 18px !important;
        height: 65px;
        font-weight: 900;
        font-size: 1.3rem;
        border: none;
        transition: 0.4s;
        box-shadow: 0 10px 25px rgba(255, 85, 0, 0.4);
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 35px rgba(255, 85, 0, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI ENGINE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Setup Error: Google API Key missing."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Create a detailed and professional travel plan for {query} in {lang}. Include daily highlights and estimated budget.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. HERO SECTION ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ ప్రయాణ అనుభవాన్ని మార్చే సరికొత్త AI ప్లానర్</p>', unsafe_allow_html=True)

# --- 5. SEARCH AREA ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (ఉదా: 5 days in Maldives...)")
    generate = st.button("Explore Now 🚀")

# --- 6. POPULAR DESTINATIONS ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 35px; font-weight: 800;'>📍 Top Trending Destinations</h2>", unsafe_allow_html=True)
    
    dests = [
        {"name": "Paris", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=500"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=500"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=500"},
        {"name": "Switzerland", "url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=500"},
        {"name": "Maldives", "url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?q=80&w=500"},
        {"name": "Manali", "url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=500"},
        {"name": "Jaipur", "url": "https://images.unsplash.com/photo-1477587458883-47145ed94245?q=80&w=500"},
        {"name": "Goa", "url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?q=80&w=500"}
    ]

    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < 8:
                with cols[j]:
                    st.markdown(f"""
                        <div class="dest-card">
                            <div class="img-container">
                                <img src="{dests[idx]['url']}" class="dest-img">
                            </div>
                            <div class="dest-label">{dests[idx]['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 7. RESULT INTERFACE ---
if generate and user_query:
    with st.status("🛠️ Creating your personal roadmap...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div style="background:rgba(255,255,255,0.95); color:#111; padding:50px; border-radius:30px; border-left:18px solid #FF9933; box-shadow: 0 40px 100px rgba(0,0,0,0.6); font-size: 1.15rem;">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)

# --- 8. PREMIUM FOOTER ---
st.markdown(f"""
    <div style="background: rgba(0, 0, 0, 0.7); padding: 50px; border-radius: 35px; margin-top: 100px; border: 1px solid rgba(255, 153, 51, 0.2); color: white;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 40px;">
            <div style="flex: 2; min-width: 300px;">
                <h2 style="color:#FF9933;">🚩 Yatri Mate AI</h2>
                <p style="opacity: 0.8;">మీ నమ్మకమైన ట్రావెల్ పార్ట్నర్.</p>
                <p style="margin-top: 25px;"><b>📍 Location:</b> Saidabad, Hyderabad, 500059</p>
            </div>
            <div style="flex: 1; min-width: 250px; text-align: right;">
                <p><b>📞 Mobile:</b> +91-6304001323</p>
                <p><b>✉️ Email:</b> veerababu.veera1@gmail.com</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Your Global Travel Partner",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                    url("https://images.unsplash.com/photo-1503220317375-aaad61436b1b?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 3.8rem !important;
        font-weight: 900;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 40px;
        font-weight: 500;
    }
    
    /* Destination Cards Enhancement */
    .dest-card {
        background: #151515;
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 153, 51, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 280px;
        display: flex;
        flex-direction: column;
        margin-bottom: 25px;
    }
    .dest-card:hover {
        transform: translateY(-12px);
        border-color: #FF9933;
        box-shadow: 0 15px 35px rgba(255, 153, 51, 0.2);
    }
    .img-container {
        width: 100%;
        height: 190px;
        background: #252525;
    }
    .dest-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .dest-label {
        padding: 18px;
        color: white;
        font-weight: 700;
        text-align: center;
        background: #000;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #FF5500 100%) !important;
        color: white !important;
        width: 100%;
        border-radius: 14px !important;
        height: 58px;
        font-weight: 800;
        font-size: 1.2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 85, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI ENGINE (Gemini 1.5 Flash) ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Error: API Key missing in setup."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Create a premium travel itinerary for {query} in {lang}. Include daily plans, hidden gems, and local food suggestions.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. MAIN HEADER ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ ప్రయాణ కలలను నిజం చేసే ఏకైక వేదిక | Best Prices Guaranteed</p>', unsafe_allow_html=True)

# --- 5. SEARCH ENGINE ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (ఉదా: 5 days trip to Ladakh...)")
    generate = st.button("Generate My Dream Plan 🚀")

# --- 6. NEW & IMPROVED DESTINATIONS ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 30px; font-weight: 800;'>📍 Popular Destinations 2026</h2>", unsafe_allow_html=True)
    
    # 8 New Reliable Destinations (Replaced Singapore, Vizag, Araku, etc.)
    dests = [
        {"name": "Paris", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=500"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=500"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=500"},
        {"name": "Switzerland", "url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=500"},
        {"name": "Hampi", "url": "https://images.unsplash.com/photo-1581333100576-b73bbe92c19a?q=80&w=500"},
        {"name": "Ooty", "url": "https://images.unsplash.com/photo-1590424600642-49110496156e?q=80&w=500"},
        {"name": "Ladakh", "url": "https://images.unsplash.com/photo-1581791534721-e599df4417f7?q=80&w=500"},
        {"name": "Varanasi", "url": "https://images.unsplash.com/photo-1561359313-0639aad49ca6?q=80&w=500"}
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
                                <img src="{dests[idx]['url']}" class="dest-img" 
                                     onerror="this.onerror=null;this.src='https://via.placeholder.com/400x200/111/FF9933?text={dests[idx]['name']}';">
                            </div>
                            <div class="dest-label">{dests[idx]['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 7. RESULT DISPLAY ---
if generate and user_query:
    with st.status("🛠️ Designing your professional itinerary...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div style="background:#fff; color:#000; padding:45px; border-radius:24px; border-left:14px solid #FF9933; box-shadow: 0 25px 60px rgba(0,0,0,0.4); line-height: 1.6;">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)

# --- 8. PROFESSIONAL FOOTER ---
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.03); padding: 50px; border-radius: 25px; margin-top: 70px; border-top: 1px solid rgba(255, 153, 51, 0.3); color: white;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px;">
            <div style="flex: 2; min-width: 300px;">
                <h2 style="color:#FF9933; margin-bottom: 10px;">🚩 Yatri Mate</h2>
                <p style="font-size: 1rem; opacity: 0.8;">Creating seamless travel experiences since 2024. Your comfort, our priority.</p>
                <p style="margin-top: 15px;"><b>Address:</b> Teen Manzil Colony, Saidabad Main road, Hyderabad, Telangana 500059</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: right;">
                <h4 style="color:#FF9933;">Contact Details</h4>
                <p><b>Mobile:</b> +91-6304001323</p>
                <p><b>Email:</b> veerababu.veera1@gmail.com</p>
                <div style="margin-top: 20px;">
                    <a href="https://yatrimate.streamlit.app/" style="color:#FF9933; text-decoration:none; font-weight:bold;">🏠 Home</a> | 
                    <span style="opacity:0.6;"> Privacy Policy</span>
                </div>
            </div>
        </div>
        <p style='text-align: center; color: rgba(255,255,255,0.4); font-size: 0.9rem; margin-top: 40px;'>© 2026 Yatri Mate AI. All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)

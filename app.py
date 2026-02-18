import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Travel Engine",
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
        background: linear-gradient(rgba(0, 0, 0, 0.82), rgba(0, 0, 0, 0.92)), 
                    url("https://images.unsplash.com/photo-1436491865332-7a61a109c0f2?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 3.8rem !important;
        font-weight: 900;
        margin-bottom: 5px;
        letter-spacing: -1.5px;
        text-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 40px;
        font-weight: 500;
        letter-spacing: 1px;
    }
    
    /* Destination Cards - Ultra Modern */
    .dest-card {
        background: #121212;
        border-radius: 22px;
        overflow: hidden;
        border: 1px solid rgba(255, 153, 51, 0.2);
        transition: all 0.4s ease-in-out;
        height: 280px;
        display: flex;
        flex-direction: column;
        margin-bottom: 30px;
    }
    .dest-card:hover {
        transform: translateY(-12px) scale(1.02);
        border-color: #FF9933;
        box-shadow: 0 20px 40px rgba(255, 153, 51, 0.15);
    }
    .img-container {
        width: 100%;
        height: 195px;
        background: #1a1a1a;
    }
    .dest-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .dest-label {
        padding: 16px;
        color: white;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(to bottom, #000000, #151515);
        font-size: 1.05rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* Professional Button */
    div.stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #FF5500 100%) !important;
        color: white !important;
        width: 100%;
        border-radius: 15px !important;
        height: 60px;
        font-weight: 800;
        font-size: 1.25rem;
        border: none;
        transition: 0.3s;
        box-shadow: 0 8px 20px rgba(255, 85, 0, 0.3);
    }
    div.stButton > button:hover {
        box-shadow: 0 12px 25px rgba(255, 85, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI CORE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Configuration Error: API Key missing."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Provide a professional travel itinerary for {query} in {lang}. Include daily highlights and estimated budget in INR.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. HEADER ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ప్రపంచాన్ని చుట్టేయండి - స్మార్ట్‌గా, హాయిగా | 2026 Trending Edition</p>', unsafe_allow_html=True)

# --- 5. SEARCH ENGINE ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఉదా: 5 రోజుల మాల్దీవుల యాత్ర ప్లాన్...")
    generate = st.button("Create My Itinerary 🚀")

# --- 6. REFRESHED DESTINATIONS (Maldives & Manali Added) ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 30px; font-weight: 800;'>📍 Top Picks for You</h2>", unsafe_allow_html=True)
    
    # 8 Fresh & High-Reliability Destinations
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
                                <img src="{dests[idx]['url']}" class="dest-img" 
                                     onerror="this.onerror=null;this.src='https://via.placeholder.com/400x200/111/FF9933?text={dests[idx]['name']}';">
                            </div>
                            <div class="dest-label">{dests[idx]['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 7. RESULT SECTION ---
if generate and user_query:
    with st.status("🛠️ Designing your personal travel guide...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div style="background:#ffffff; color:#1a1a1a; padding:45px; border-radius:25px; border-left:15px solid #FF9933; box-shadow: 0 30px 70px rgba(0,0,0,0.5); font-size: 1.1rem; line-height: 1.7;">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)
    st.download_button("📥 Download Itinerary (MD)", st.session_state.itinerary_data, file_name="YatriMate_Plan.md")

# --- 8. FOOTER ---
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.04); padding: 50px; border-radius: 30px; margin-top: 80px; border-top: 1px solid rgba(255, 153, 51, 0.2); color: white;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 40px;">
            <div style="flex: 2; min-width: 300px;">
                <h2 style="color:#FF9933; margin-bottom: 15px;">🚩 Yatri Mate</h2>
                <p style="opacity: 0.8; line-height: 1.6;">మీ ప్రయాణ అవసరాల కోసం అత్యంత విశ్వసనీయమైన AI పార్ట్నర్. మేము కేవలం ప్లాన్స్ మాత్రమే కాదు, మధురమైన జ్ఞాపకాలను అందిస్తాము.</p>
                <p style="margin-top: 20px;"><b>📍 Address:</b> Teen Manzil Colony, Saidabad Main road, Hyderabad, Telangana 500059</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: right;">
                <h4 style="color:#FF9933; margin-bottom: 15px;">Contact Us</h4>
                <p><b>📞 Mobile:</b> +91-6304001323</p>
                <p><b>✉️ Email:</b> veerababu.veera1@gmail.com</p>
                <div style="margin-top: 25px;">
                    <a href="https://yatrimate.streamlit.app/" style="color:#FF9933; text-decoration:none; font-weight:bold; border: 1px solid #FF9933; padding: 8px 15px; border-radius: 8px;">🏠 Home Page</a>
                </div>
            </div>
        </div>
        <p style='text-align: center; color: rgba(255,255,255,0.3); font-size: 0.85rem; margin-top: 50px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px;'>© 2026 Yatri Mate AI Engine. All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Travel Planning Redefined",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8df9?q=80&w=2021");
        background-size: cover;
        background-attachment: fixed;
    }
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }
    
    /* Permanent Image Solution */
    .dest-card {
        background: #1e1e1e;
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(255, 153, 51, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
        height: 260px;
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }
    .dest-card:hover {
        transform: translateY(-8px);
        border-color: #FF9933;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .img-box {
        width: 100%;
        height: 190px;
        background: #2d2d2d; /* Loading/Error color */
        position: relative;
    }
    .dest-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .dest-name {
        padding: 15px;
        color: white;
        font-weight: bold;
        text-align: center;
        background: #000000;
        font-size: 1rem;
    }

    /* Custom Button */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important;
        width: 100%;
        border-radius: 12px !important;
        height: 55px;
        font-weight: 800;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI CORE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Error: API Key missing in Streamlit Secrets."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Create a detailed travel itinerary for {query} in {lang}. Include tables, transport tips, and estimated costs.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. HEADER ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Trusted & Affordable</p>', unsafe_allow_html=True)

# --- 5. SEARCH SECTION ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (ఉదా: 3 days in Vizag...)")
    generate = st.button("Generate My Plan 🚀")

# --- 6. POPULAR DESTINATIONS (PERMANENTLY FIXED LINKS) ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 30px;'>📍 Popular Destinations</h2>", unsafe_allow_html=True)
    
    # Verified Static URLs
    dests = [
        {"name": "Kerala", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?q=80&w=500"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=500"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=500"},
        {"name": "Singapore", "url": "https://images.unsplash.com/photo-1525625232717-1292b236f561?q=80&w=500"},
        {"name": "Visakhapatnam", "url": "https://images.unsplash.com/photo-1594913217002-869272825126?q=80&w=500"},
        {"name": "Araku Valley", "url": "https://images.unsplash.com/photo-1623945417534-1907797709b1?q=80&w=500"},
        {"name": "Tirumala", "url": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Tirumala_090615.jpg"},
        {"name": "Gandikota", "url": "https://images.unsplash.com/photo-1647414848609-b467ec6a6d63?q=80&w=500"}
    ]

    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < 8:
                with cols[j]:
                    st.markdown(f"""
                        <div class="dest-card">
                            <div class="img-box">
                                <img src="{dests[idx]['url']}" class="dest-img" 
                                     onerror="this.onerror=null;this.src='https://via.placeholder.com/400x190/333/fff?text={dests[idx]['name']}';">
                            </div>
                            <div class="dest-name">{dests[idx]['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 7. RESULTS ---
if generate and user_query:
    with st.status("🛠️ Designing your itinerary...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div style="background:white; color:black; padding:40px; border-radius:20px; border-left:10px solid #FF9933;">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; margin-top: 60px; border-top: 1px solid #FF9933; color: white;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px;">
                <h3 style="color:#FF9933;">🚩 Yatri Mate</h3>
                <p>Teen Manzil Colony, Saidabad Main road, Hyderabad, Telangana 500059</p>
            </div>
            <div style="flex: 1; min-width: 250px; text-align: right;">
                <p><b>Mobile:</b> +91-6304001323</p>
                <p><b>Email:</b> veerababu.veera1@gmail.com</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

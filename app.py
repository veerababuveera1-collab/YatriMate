import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Global Travel Planner",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SENIOR-ENGINEER UI STYLING ---
st.markdown("""
    <style>
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.95)), 
                    url("https://images.unsplash.com/photo-1488646953014-85cb44e25828?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 2px 2px 15px rgba(0,0,0,0.5);
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }
    
    /* Destination Cards - Robust UI */
    .dest-card {
        background: #111111;
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255, 153, 51, 0.2);
        transition: 0.4s ease;
        height: 280px;
        display: flex;
        flex-direction: column;
        margin-bottom: 25px;
    }
    .dest-card:hover {
        transform: translateY(-10px);
        border-color: #FF9933;
        box-shadow: 0 12px 25px rgba(255, 153, 51, 0.15);
    }
    .img-area {
        width: 100%;
        height: 200px;
        background: #222222; /* Loading Fallback Color */
        position: relative;
    }
    .dest-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .dest-info {
        padding: 15px;
        color: white;
        font-weight: bold;
        text-align: center;
        background: #000000;
        font-size: 1.1rem;
    }

    /* Generator Button */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important;
        width: 100%;
        border-radius: 12px !important;
        height: 55px;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI ENGINE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "API Key Error: Please check secrets.toml"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Travel itinerary for {query} in {lang}. Include budget and time tables.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. HEADER ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Reliable & Affordable</p>', unsafe_allow_html=True)

# --- 5. USER INPUT ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (ఉదా: 3 days in Vizag & Araku...)")
    generate = st.button("Get My Custom Plan 🚀")

# --- 6. POPULAR DESTINATIONS (HIGH-RELIABILITY LINKS) ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 30px;'>📍 Popular Destinations</h2>", unsafe_allow_html=True)
    
    # Using Static High-Uptime CDNs
    dests = [
        {"name": "Kerala", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?q=80&w=500"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=500"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=500"},
        {"name": "Singapore", "url": "https://images.unsplash.com/photo-1525625232717-1292b236f561?q=80&w=500"},
        {"name": "Visakhapatnam", "url": "https://images.unsplash.com/photo-1594913217002-869272825126?q=80&w=500"},
        {"name": "Araku Valley", "url": "https://images.unsplash.com/photo-1623945417534-1907797709b1?q=80&w=500"},
        # Tirumala Fix: High Quality Wikimedia Link
        {"name": "Tirumala", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tirumala_090615.jpg/800px-Tirumala_090615.jpg"},
        # Gandikota Fix: Gorge View
        {"name": "Gandikota", "url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?q=80&w=500"}
    ]

    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < 8:
                with cols[j]:
                    st.markdown(f"""
                        <div class="dest-card">
                            <div class="img-area">
                                <img src="{dests[idx]['url']}" class="dest-img" 
                                     onerror="this.onerror=null;this.src='https://via.placeholder.com/400x200/111111/FF9933?text={dests[idx]['name']}';">
                            </div>
                            <div class="dest-info">{dests[idx]['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 7. RESULTS ---
if generate and user_query:
    with st.status("🛠️ Designing your personal guide...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div style="background:white; color:black; padding:40px; border-radius:20px; border-left:12px solid #FF9933;">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)

# --- 8. FOOTER (UPDATED CONTACT) ---
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; margin-top: 60px; border-top: 1px solid #FF9933; color: white;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px;">
                <h3 style="color:#FF9933;">🚩 Yatri Mate</h3>
                <p>Teen Manzil Colony, Saidabad Main road,<br>Hyderabad, Telangana 500059</p>
            </div>
            <div style="flex: 1; min-width: 250px; text-align: right;">
                <p><b>Mobile:</b> +91-6304001323</p>
                <p><b>Email:</b> veerababu.veera1@gmail.com</p>
                <p><a href="https://yatrimate.streamlit.app/" style="color:#FF9933; text-decoration:none;">🏠 Back to Home</a></p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

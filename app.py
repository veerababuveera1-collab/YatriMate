import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Enterprise Travel Engine",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM GUI STYLING ---
st.markdown("""
    <style>
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                    url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }
    
    /* Permanent Image Fix Styling */
    .dest-card {
        background: #1A1A1A;
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(255, 153, 51, 0.2);
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 250px;
        display: flex;
        flex-direction: column;
    }
    .dest-card:hover {
        transform: translateY(-10px);
        border-color: #FF9933;
        box-shadow: 0 15px 30px rgba(255, 153, 51, 0.2);
    }
    .img-wrapper {
        width: 100%;
        height: 180px;
        background: #2D2D2D; /* Fallback color */
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
        letter-spacing: 0.5px;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important;
        width: 100%;
        border-radius: 12px !important;
        height: 55px;
        font-weight: 800;
        border: none;
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI ENGINE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Error: API Key missing in Secrets."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Travel itinerary for {query} in {lang}. Include tables and local tips.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Affordable Journeys</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఉదా: 4 రోజుల వైజాగ్ మరియు అరకు యాత్ర ప్లాన్...")
    generate = st.button("Generate My Itinerary 🚀")

# --- 5. POPULAR DESTINATIONS (THE PERMANENT FIX) ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 40px;'>📍 Popular Destinations</h2>", unsafe_allow_html=True)
    
    # Data with Verified High-Uptime CDN Links
    destinations = [
        {"name": "Kerala", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=400&h=250"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=400&h=250"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=400&h=250"},
        {"name": "Singapore", "url": "https://images.unsplash.com/photo-1525625232717-1292b236f561?auto=format&fit=crop&w=400&h=250"},
        {"name": "Visakhapatnam", "url": "https://images.unsplash.com/photo-1594913217002-869272825126?auto=format&fit=crop&w=400&h=250"},
        {"name": "Araku Valley", "url": "https://images.unsplash.com/photo-1623945417534-1907797709b1?auto=format&fit=crop&w=400&h=250"},
        {"name": "Tirumala", "url": "https://images.unsplash.com/photo-1614088685112-0a760b71a3c8?auto=format&fit=crop&w=400&h=250"},
        {"name": "Gandikota", "url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=400&h=250"}
    ]

    # Grid Display
    for i in range(0, len(destinations), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(destinations):
                d = destinations[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="dest-card">
                            <div class="img-wrapper">
                                <img src="{d['url']}" class="dest-img" alt="{d['name']}"
                                     onerror="this.style.display='none';">
                            </div>
                            <div class="dest-name">{d['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 6. RESULTS & FOOTER ---
if generate and user_query:
    with st.status("🛠️ Engineering your travel plan...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div style="background:white; color:black; padding:40px; border-radius:20px; border-left:12px solid #FF9933; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; margin-top: 60px; border-top: 1px solid #FF9933;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; color: white;">
            <div style="flex: 1; min-width: 250px; margin-bottom: 20px;">
                <h3 style="color:#FF9933;">🚩 Yatri Mate</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">Making the world accessible for everyone with comfortable stays and guided tours.</p>
            </div>
            <div style="flex: 1; min-width: 250px; margin-bottom: 20px;">
                <h3 style="color:#FF9933;">📍 Contact Us</h3>
                <p style="font-size: 0.9rem;">Teen Manzil Colony, Saidabad Main road, Hyderabad, Telangana 500059</p>
                <p style="font-size: 0.9rem;"><b>Mobile:</b> +91-6304001323</p>
                <p style="font-size: 0.9rem;"><b>Email:</b> veerababu.veera1@gmail.com</p>
            </div>
        </div>
        <p style='text-align: center; color: grey; font-size: 0.8rem; margin-top: 20px;'>Copyright © 2026 - Yatri Mate</p>
    </div>
""", unsafe_allow_html=True)

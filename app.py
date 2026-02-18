import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Enterprise Travel Engine",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SENIOR-GRADE GUI STYLING ---
st.markdown("""
    <style>
    * { font-family: 'Inter', -apple-system, sans-serif; }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }

    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 4rem !important;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 0px;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .sub-title {
        color: rgba(255,255,255,0.8) !important;
        text-align: center;
        font-size: 1.2rem;
        margin-top: -10px;
        margin-bottom: 40px;
    }

    /* Destination Card Styling */
    .dest-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .dest-card:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.25);
        border: 1px solid #FF9933;
    }
    .dest-name {
        color: white;
        font-weight: bold;
        margin-top: 10px;
        font-size: 1.1rem;
    }

    div.stButton { text-align: center; margin-top: 20px; }
    div.stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #FF5500 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        height: 55px !important;
        width: 280px !important;
        border: none !important;
        border-radius: 12px !important;
    }

    .itinerary-card {
        background: #FFFFFF !important;
        color: #1A1A1A !important;
        padding: 40px;
        border-radius: 20px;
        margin-top: 40px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.4);
        border-left: 10px solid #FF9933;
    }

    .footer-box {
        background: rgba(255, 255, 255, 0.03);
        padding: 40px;
        border-radius: 20px;
        margin-top: 60px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE AI ENGINE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Error: API Key missing."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Professional Travel Itinerary for {query} in {lang}. Include tables, budget, and local food tips.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Affordable Journeys</p>', unsafe_allow_html=True)

# --- SEARCH BOX ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఉదా: 3 రోజుల విశాఖపట్నం యాత్ర ప్లాన్...")
    generate = st.button("Generate My Itinerary 🚀")

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. POPULAR DESTINATIONS (AP & WORLD) ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-bottom: 25px;'>📍 Popular Destinations</h2>", unsafe_allow_html=True)
    
    # 1st Row: International/Popular
    row1_c1, row1_c2, row1_c3, row1_c4 = st.columns(4)
    dest_row1 = [
        {"name": "Kerala", "img": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400&h=250&fit=crop"},
        {"name": "Dubai", "img": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop"},
        {"name": "Bali", "img": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=250&fit=crop"},
        {"name": "Singapore", "img": "https://images.unsplash.com/photo-1525625232717-1292b236f561?w=400&h=250&fit=crop"}
    ]
    
    # 2nd Row: Andhra Pradesh Focus
    st.markdown("<p style='text-align: center; color: #FF9933; font-weight: bold; margin-top: 30px;'>EXPLORE ANDHRA PRADESH</p>", unsafe_allow_html=True)
    row2_c1, row2_c2, row2_c3, row2_c4 = st.columns(4)
    dest_row2 = [
        {"name": "Visakhapatnam", "img": "https://images.unsplash.com/photo-1594913217002-869272825126?w=400&h=250&fit=crop"},
        {"name": "Araku Valley", "img": "https://images.unsplash.com/photo-1623945417534-1907797709b1?w=400&h=250&fit=crop"},
        {"name": "Tirumala", "img": "https://images.unsplash.com/photo-1614088685112-0a760b71a3c8?w=400&h=250&fit=crop"},
        {"name": "Gandikota", "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400&h=250&fit=crop"}
    ]
    
    # Rendering Logic
    all_cols = [row1_c1, row1_c2, row1_c3, row1_c4, row2_c1, row2_c2, row2_c3, row2_c4]
    all_dests = dest_row1 + dest_row2
    
    for i, d in enumerate(all_dests):
        with all_cols[i]:
            st.markdown(f'''
                <div class="dest-card">
                    <img src="{d['img']}" style="width:100%; border-radius:10px; height:150px; object-fit:cover;">
                    <div class="dest-name">{d['name']}</div>
                </div>
            ''', unsafe_allow_html=True)

# --- 6. EXECUTION & RESULTS ---
if generate and user_query:
    with st.status("🛠️ Engineering your travel plan...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div class="itinerary-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button("📥 Export Guide", st.session_state.itinerary_data, file_name="YatriMate_Plan.md")

# --- 7. FOOTER ---
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
f1, f2, f3 = st.columns([2, 1, 2])
with f1:
    st.markdown("### 🚩 Yatri Mate")
    st.write("Making the world accessible for everyone with comfortable stays and guided tours.")
with f2:
    st.markdown("### 🔗 Links")
    st.write("• [Home](https://yatrimate.streamlit.app/)\n\n• About Us\n\n• Contact Us")
with f3:
    st.markdown("### 📍 Contact Info")
    st.markdown("""
    **Address:** Teen Manzil Colony, Saidabad Main road, Hyderabad, Telangana 500059  
    **Mobile:** +91-6304001323  
    **Email:** veerababu.veera1@gmail.com
    """)
st.markdown("<p style='text-align: center; color: grey; font-size: 0.8rem; margin-top: 20px;'>Copyright © 2026 - Yatri Mate | Hyderabad</p></div>", unsafe_allow_html=True)

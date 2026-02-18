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
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                    url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 4rem !important;
        font-weight: 900;
        margin-bottom: 0px;
        text-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }
    
    /* Image Gallery Styling */
    .img-container {
        position: relative;
        text-align: center;
        color: white;
        transition: transform .4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .img-container:hover {
        transform: scale(1.08);
        z-index: 10;
    }
    .dest-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .dest-label {
        background: rgba(0, 0, 0, 0.7);
        padding: 8px;
        border-radius: 0 0 15px 15px;
        font-weight: bold;
        margin-top: -40px;
        position: relative;
        font-size: 0.9rem;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important;
        width: 100%;
        border-radius: 12px !important;
        height: 55px;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(255, 153, 51, 0.6) !important;
    }

    .itinerary-card {
        background: white !important;
        color: black !important;
        padding: 40px;
        border-radius: 25px;
        border-left: 12px solid #FF9933;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    .footer-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 20px;
        margin-top: 60px;
        border-top: 1px solid rgba(255, 153, 51, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE AI ENGINE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Error: API Key missing."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Professional Travel Itinerary for {query} in {lang}. Include daily plan tables and estimated costs.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Affordable Journeys</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (ఉదా: 4 days trip to Tirumala & Gandikota...)")
    generate = st.button("Generate My Itinerary 🚀")

# --- 5. UPDATED POPULAR DESTINATIONS ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 40px;'>📍 Popular Destinations</h2>", unsafe_allow_html=True)
    
    # 1st Row: International
    col1, col2, col3, col4 = st.columns(4)
    row1 = [
        {"name": "Kerala", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=500&q=80"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=500&q=80"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=500&q=80"},
        {"name": "Singapore", "url": "https://images.unsplash.com/photo-1525625232717-1292b236f561?auto=format&fit=crop&w=500&q=80"}
    ]
    
    # 2nd Row: Andhra Pradesh Focus (With Correct Gandikota Image)
    st.markdown("<p style='text-align: center; color: #FF9933; font-weight: bold; margin-top: 30px; font-size: 1.2rem;'>EXPLORE ANDHRA PRADESH</p>", unsafe_allow_html=True)
    col5, col6, col7, col8 = st.columns(4)
    row2 = [
        {"name": "Visakhapatnam", "url": "https://images.unsplash.com/photo-1594913217002-869272825126?auto=format&fit=crop&w=500&q=80"},
        {"name": "Araku Valley", "url": "https://images.unsplash.com/photo-1623945417534-1907797709b1?auto=format&fit=crop&w=500&q=80"},
        {"name": "Tirumala", "url": "https://images.unsplash.com/photo-1614088685112-0a760b71a3c8?auto=format&fit=crop&w=500&q=80"},
        # Updated Gandikota Image
        {"name": "Gandikota", "url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=500&q=80"}
    ]

    all_cols = [col1, col2, col3, col4, col5, col6, col7, col8]
    all_dests = row1 + row2

    for i, dest in enumerate(all_dests):
        with all_cols[i]:
            st.markdown(f"""
                <div class="img-container">
                    <img src="{dest['url']}" class="dest-img">
                    <div class="dest-label">{dest['name']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. RESULTS ---
if generate and user_query:
    with st.status("🛠️ Designing your custom itinerary...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div class="itinerary-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button("📥 Download Travel Guide", st.session_state.itinerary_data, file_name="YatriMate_Plan.md")

# --- 7. FOOTER (Updated Branding) ---
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
f1, f2, f3 = st.columns([2, 1, 2])
with f1:
    st.markdown("### 🚩 Yatri Mate")
    st.write("We at Yatri Mate comprehend that these days, voyaging has become considerably more than simply visiting another objective. We strive to guarantee comprehensive occasion encounters.")
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
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 30px;'>Copyright © 2026 - Yatri Mate | Hyderabad, India</p></div>", unsafe_allow_html=True)

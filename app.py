import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Travel Engine",
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
        font-size: 3.5rem !important;
        font-weight: 900;
        margin-bottom: 0px;
        text-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    /* Destination Card Styling */
    .img-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s ease;
        text-align: center;
    }
    .img-card:hover {
        transform: translateY(-5px);
        border-color: #FF9933;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    .dest-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    .dest-label {
        padding: 10px;
        color: white;
        font-weight: bold;
        background: rgba(0,0,0,0.7);
        font-size: 0.9rem;
    }

    /* Professional Button */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important;
        width: 100%;
        border-radius: 10px !important;
        height: 50px;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
    }

    .itinerary-card {
        background: white !important;
        color: black !important;
        padding: 40px;
        border-radius: 20px;
        border-left: 10px solid #FF9933;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
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
    response = model.generate_content(f"Travel itinerary for {query} in {lang}. Include daily tables and costs.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Affordable Journeys</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (ఉదా: 5 days trip to Kashi...)")
    generate = st.button("Generate My Itinerary 🚀")

# --- 5. POPULAR DESTINATIONS (FINAL FIXED IMAGES) ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 30px;'>📍 Popular Destinations</h2>", unsafe_allow_html=True)
    
    # 1st Row: International
    col1, col2, col3, col4 = st.columns(4)
    row1 = [
        {"name": "Kerala", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400&h=250&fit=crop"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=250&fit=crop"},
        {"name": "Singapore", "url": "https://images.unsplash.com/photo-1525625232717-1292b236f561?w=400&h=250&fit=crop"}
    ]
    
    # 2nd Row: Andhra Pradesh Focus
    st.markdown("<p style='text-align: center; color: #FF9933; font-weight: bold; margin-top: 20px;'>EXPLORE ANDHRA PRADESH</p>", unsafe_allow_html=True)
    col5, col6, col7, col8 = st.columns(4)
    row2 = [
        {"name": "Visakhapatnam", "url": "https://images.unsplash.com/photo-1594913217002-869272825126?w=400&h=250&fit=crop"},
        {"name": "Araku Valley", "url": "https://images.unsplash.com/photo-1623945417534-1907797709b1?w=400&h=250&fit=crop"},
        {"name": "Tirumala", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tirumala_090615.jpg/400px-Tirumala_090615.jpg"},
        {"name": "Gandikota", "url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400&h=250&fit=crop"}
    ]

    all_cols = [col1, col2, col3, col4, col5, col6, col7, col8]
    all_dests = row1 + row2

    for i, dest in enumerate(all_dests):
        with all_cols[i]:
            st.markdown(f"""
                <div class="img-card">
                    <img src="{dest['url']}" class="dest-img" onerror="this.src='https://via.placeholder.com/400x250?text={dest['name']}';">
                    <div class="dest-label">{dest['name']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. EXECUTION & RESULTS ---
if generate and user_query:
    with st.status("🛠️ Designing your custom itinerary...", expanded=False):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div class="itinerary-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button("📥 Export Travel Guide", st.session_state.itinerary_data, file_name="YatriMate_Plan.md")

# --- 7. FOOTER SECTION ---
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
f1, f2, f3 = st.columns([2, 1, 2])
with f1:
    st.markdown("### 🚩 Yatri Mate")
    st.write("We strive to guarantee comprehensive occasion encounters. Affordable stays, transport, and guided tours for everyone.")
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

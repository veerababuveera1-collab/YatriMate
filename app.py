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
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2000");
        background-size: cover;
        background-attachment: fixed;
    }

    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 4.5rem !important;
        font-weight: 900;
        letter-spacing: -2px;
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

    div.stButton { text-align: center; margin-top: 20px; }
    div.stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #FF5500 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        height: 60px !important;
        width: 320px !important;
        border: none !important;
        border-radius: 14px !important;
        font-size: 1.2rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 25px rgba(255, 85, 0, 0.3) !important;
    }

    .itinerary-card {
        background: #FFFFFF !important;
        color: #1A1A1A !important;
        padding: 50px;
        border-radius: 24px;
        margin-top: 40px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.4);
        border-left: 12px solid #FF9933;
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
    if not api_key:
        return "Error: API Key missing."
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Professional travel agent itinerary for {query} in {lang}. Include tables."
    response = model.generate_content(prompt)
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/map-marker.png")
    st.markdown("## 🌐 Global Settings")
    selected_lang = st.selectbox("Preferred Language:", ["Telugu & English Mix", "Pure Telugu", "English", "Hindi"])
    st.divider()
    if st.button("🔄 Reset Environment"):
        st.session_state.itinerary_data = None
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Affordable Journeys & Guided Experiences</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="Where to? (e.g., 5 days trip to Kashi...)")
    generate = st.button("Generate My Itinerary 🚀")

if generate and user_query:
    with st.status("🛠️ Engineering your travel plan...", expanded=False) as status:
        result = generate_travel_plan(user_query, selected_lang)
        st.session_state.itinerary_data = result
        status.update(label="Itinerary Synthesized! ✅", state="complete")

if st.session_state.itinerary_data:
    st.markdown(f'<div class="itinerary-card">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. UPDATED FOOTER SECTION ---
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
f1, f2, f3 = st.columns([2, 1, 2])

with f1:
    st.markdown("### 🚩 Yatri Mate")
    st.write("We strive to make the world accessible for each and every one! Comfortable stay, transport, and abundant sightseeing on every tour.")

with f2:
    st.markdown("### 🔗 Links")
    # Removed Hyperlinks for About and Contact
    st.write(f"• [Home](https://yatrimate.streamlit.app/)\n\n• About Us\n\n• Contact Us")

with f3:
    st.markdown("### 📍 Contact Info")
    # Updated Address, Email, and Mobile
    st.markdown(f"""
    **Address:** Teen Manzil Colony, Saidabad Main road, Hyderabad, Telangana 500059  
    
    **Mobile:** +91-6304001323  
    
    **Email:** veerababu.veera1@gmail.com
    """)

st.markdown("""
    <p style='text-align: center; color: rgba(255,255,255,0.4); font-size: 0.8rem; margin-top: 30px;'>
        Copyright © 2026 - Yatri Mate | Hyderabad, India | Built with ❤️ for Travelers
    </p>
    </div>
    """, unsafe_allow_html=True)

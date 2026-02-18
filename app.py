import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Premium Travel Guide", 
    page_icon="🚩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CSS (Centered Elements & High Readability) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Header Styling */
    .header-text {
        color: #FFFFFF !important;
        text-align: center;
        text-shadow: 2px 2px 15px rgba(0,0,0,1);
        font-weight: 800;
        margin-top: -20px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.98);
        border-right: 5px solid #FF9933;
    }

    /* Centering the Button Container */
    .stButton {
        display: flex;
        justify-content: center;
    }
    
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF7700) !important;
        color: white !important;
        font-weight: bold !important;
        height: 55px;
        width: 300px !important; /* Fixed width for better centering look */
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        transition: 0.3s all;
        box-shadow: 0 4px 15px rgba(255, 120, 0, 0.4);
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 120, 0, 0.6);
    }

    /* White Result Card */
    .itinerary-container {
        background: #FFFFFF !important; 
        padding: 40px;
        border-radius: 20px;
        color: #1A1A1A !important;
        line-height: 1.8;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        border-left: 10px solid #FF9933;
        margin-top: 30px;
    }

    /* Input Box Focus */
    .stTextInput input {
        border-radius: 10px !important;
        border: 2px solid #FF9933 !important;
        text-align: center;
    }

    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI ENGINE ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("API Key missing! Please check your secrets.")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. SIDEBAR (Instructions & Contact) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/around-the-globe.png")
    st.markdown("### 🌐 Settings")
    selected_lang = st.selectbox("Language / భాష:", ["Telugu & English Mix", "Pure Telugu", "English", "Hindi"])
    
    st.divider()
    st.markdown("### 📞 Support")
    st.info("Need help? Call: +91 7057483149")
    st.write("📧 info@yatrimate.com")
    
    st.divider()
    if st.button("🔄 Reset App"):
        st.session_state.itinerary_data = None
        st.rerun()

# --- 5. UI LAYOUT ---
st.markdown('<h1 class="header-text" style="font-size: 4rem;">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-text" style="font-size: 1.4rem; margin-bottom: 40px;">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Affordable Journeys</p>', unsafe_allow_html=True)

# --- 6. INPUT SECTION (Centered) ---
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    user_query = st.text_input("ఎక్కడికి వెళ్లాలనుకుంటున్నారు?", placeholder="ఉదా: 4 days trip to Kerala with family...")
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # The "Middle" button logic
    generate = st.button("Generate My Itinerary 🚀")

# --- 7. PROCESSING & RESULTS ---
if generate and user_query:
    model = get_gemini_model()
    if model:
        with st.status("YatriMate Agents are planning your trip...", expanded=False) as status:
            prompt = f"Create a professional, detailed travel itinerary for {user_query} in {selected_lang}. Include tables for daily plans and budget estimates."
            response = model.generate_content(prompt)
            st.session_state.itinerary_data = response.text
            status.update(label="Itinerary Ready! ✅", state="complete")

if st.session_state.itinerary_data:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Centered Download Button
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("Download Plan (PDF/Text) 📥", st.session_state.itinerary_data, file_name="YatriMate_Plan.md")

# --- 8. FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; color: white; opacity: 0.7;'>
        Copyright © 2026 - Yatri Mate | Kalyan, Thane, Maharashtra<br>
        <i>We strive to make the world accessible for each and every one!</i>
    </p>
    """, unsafe_allow_html=True)

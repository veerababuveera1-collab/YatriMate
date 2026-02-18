import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Guide", 
    page_icon="🚩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    .header-text {
        color: #FFFFFF !important;
        text-align: center;
        text-shadow: 2px 2px 15px rgba(0,0,0,1);
        font-weight: 800;
        margin-top: -30px;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.98);
        border-right: 5px solid #FF9933;
    }

    .itinerary-container {
        background: #FFFFFF !important; 
        padding: 40px;
        border-radius: 15px;
        color: #000000 !important;
        line-height: 1.8;
        font-size: 1.15rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        border-left: 10px solid #FF9933;
        margin-top: 20px;
    }

    /* Button alignment fix */
    div.stButton {
        text-align: center;
    }
    
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF7700) !important;
        color: white !important;
        font-weight: bold !important;
        height: 55px;
        padding: 0 40px !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
    }

    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ENGINE ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("API Key missing!")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🌐 Settings")
    selected_lang = st.selectbox("Language:", ["Telugu & English Mix", "Pure Telugu", "English", "Hindi"])
    st.divider()
    st.markdown("## 🤖 AI Agents")
    st.write("🗺️ Planner | 🔍 Researcher | ✍️ Writer")
    if st.button("Reset Everything"):
        st.session_state.itinerary_data = None
        st.rerun()

# --- 5. UI LAYOUT ---
st.markdown('<h1 class="header-text" style="font-size: 3.5rem;">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-text" style="font-size: 1.3rem; margin-bottom: 30px;">మీ పర్సనల్ ట్రావెల్ ఏజెంట్</p>', unsafe_allow_html=True)

# --- 6. INPUT SECTION (Centered) ---
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    user_query = st.text_input("ప్రయాణ వివరాలు తెలపండి:", placeholder="ఉదా: 3 రోజుల అమరావతి యాత్ర ప్లాన్...")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Button is now centered within this column
    generate = st.button("Generate My Itinerary 🚀")

# --- 7. PROCESSING & RESULTS ---
if generate and user_query:
    model = get_gemini_model()
    if model:
        with st.status("ఏజెంట్లు పనిచేస్తున్నారు...", expanded=False) as status:
            final = model.generate_content(f"Create a high-quality travel guide for {user_query} in {selected_lang}").text
            st.session_state.itinerary_data = final
            status.update(label="ప్లాన్ సిద్ధం! ✅", state="complete")

if st.session_state.itinerary_data:
    st.markdown(f'<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    st.download_button("Download Full Guide 📥", st.session_state.itinerary_data, file_name="My_Travel_Plan.md")

st.markdown("<br><p style='text-align: center; color: white; opacity: 0.6;'>YatriMate AI © 2026</p>", unsafe_allow_html=True)

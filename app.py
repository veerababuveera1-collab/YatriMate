import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Guide", 
    page_icon="🚩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GUI WITH DARK OVERLAY & ANIMATIONS ---
st.markdown("""
    <style>
    /* Background with Dark Overlay */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Global Text Colors */
    html, body, [class*="st-"], p, span, label {
        color: #1A1A1A !important; 
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }

    /* Header Styling */
    .header-text {
        color: #FFFFFF !important;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.9);
    }

    /* Sidebar Styling & Animation */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-right: 3px solid #FF9933;
    }

    /* Simple Icon Animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .animate-icon {
        display: inline-block;
        animation: pulse 2s infinite;
        font-size: 1.5rem;
    }

    /* High-Contrast Result Container */
    .itinerary-container {
        background: rgba(255, 255, 255, 0.98) !important; 
        padding: 40px;
        border-radius: 15px;
        color: #000000 !important;
        line-height: 1.8;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        border-left: 8px solid #FF9933;
    }

    /* Table Styling */
    table { width: 100%; background-color: white !important; color: black !important; }
    th { background-color: #f1f1f1 !important; color: black !important; font-weight: bold; }
    td { border-bottom: 1px solid #eee !important; color: black !important; }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF7700) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ENGINE ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3-flash-preview')

# --- 4. SESSION STATE ---
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 5. SIDEBAR (Instructions & Agents) ---
with st.sidebar:
    st.markdown("## ⚙️ How to Use")
    st.markdown("""
    1. **Enter Destination:** పైన ఉన్న బాక్స్‌లో మీ గమ్యాన్ని (ఉదా: 'Vizag trip for 3 days') టైప్ చేయండి.
    2. **Click Generate:** 'Generate My Itinerary' బటన్ నొక్కండి.
    3. **Wait for Agents:** మా AI ఏజెంట్లు మీ ప్లాన్ సిద్ధం చేసే వరకు ఆగండి.
    4. **Download:** ప్లాన్ నచ్చితే చివరలో ఉన్న డౌన్‌లోడ్ బటన్ వాడండి.
    """)
    
    st.divider()
    
    st.markdown("## 🤖 Our AI Agents")
    st.markdown("""
    <div class='animate-icon'>🗺️</div> **Planner Agent:** మీ ప్రయాణ మార్గాన్ని (Route) సిద్ధం చేస్తుంది.<br><br>
    <div class='animate-icon'>🔍</div> **Researcher Agent:** ధరలు, సమయాలు మరియు వాస్తవాలను ధృవీకరిస్తుంది.<br><br>
    <div class='animate-icon'>✍️</div> **Writer Agent:** అందమైన టేబుల్స్ మరియు వివరణలతో గైడ్ రాస్తుంది.
    """, unsafe_allow_html=True)
    
    st.divider()
    if st.button("Reset / Clear All"):
        st.session_state.itinerary_data = None
        st.rerun()

# --- 6. UI LAYOUT ---
st.markdown('<h1 class="header-text" style="font-size: 4rem; margin-bottom:0;">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-text" style="font-size: 1.3rem; margin-bottom: 40px;">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ - Gemini 3 Edition</p>', unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    # Input Area
    st.markdown("<div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);'>", unsafe_allow_html=True)
    user_query = st.text_input("ప్రయాణ వివరాలు తెలపండి:", placeholder="ఉదా: 3 రోజుల అమరావతి యాత్ర ప్లాన్...")
    generate = st.button("Generate My Itinerary 🚀")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. PROCESSING ---
if generate and user_query:
    model = get_gemini_model()
    if model:
        with st.status("ఏజెంట్లు పనిచేస్తున్నారు...", expanded=True) as status:
            st.write("🗺️ ప్లానర్: రూట్ సిద్ధం చేస్తోంది...")
            plan = model.generate_content(f"Create a day-wise itinerary for {user_query}").text
            
            st.write("🔍 రీసెర్చర్: ధరలు మరియు సమయాలు వెతుకుతోంది...")
            research = model.generate_content(f"Find entry fees and timings for: {plan}").text
            
            st.write("✍️ రైటర్: ఫైనల్ గైడ్ రాస్తోంది...")
            final = model.generate_content(f"Create a detailed travel guide with tables in Telugu and English. Use this: {research}").text
            
            st.session_state.itinerary_data = final
            status.update(label="ప్లాన్ సిద్ధంగా ఉంది! ✅", state="complete")

# --- 8. RESULTS ---
if st.session_state.itinerary_data:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.download_button("Download Guide 📥", st.session_state.itinerary_data, file_name="My_Travel_Plan.md")

st.markdown("<br><p style='text-align: center; color: white;'>YatriMate AI © 2026</p>", unsafe_allow_html=True)

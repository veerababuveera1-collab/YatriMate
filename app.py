import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Guide", 
    page_icon="🚩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE ULTIMATE READABLE GUI ---
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
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] span {
        color: #1A1A1A !important;
        font-weight: 600;
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

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    .agent-icon {
        display: inline-block;
        animation: bounce 1.5s infinite;
        font-size: 1.4rem;
        margin-right: 10px;
    }

    table { width: 100%; background: white !important; color: black !important; border: 1px solid #ddd; }
    th { background: #f0f0f0 !important; color: black !important; font-weight: bold; padding: 10px; border: 1px solid #ccc; }
    td { border: 1px solid #eee !important; color: black !important; padding: 10px; }
    
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF7700) !important;
        color: white !important;
        font-weight: bold !important;
        height: 50px;
        border: none !important;
        width: 100%;
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
        st.error("API Key missing! Check secrets.")
        return None
    genai.configure(api_key=api_key)
    # Using stable flash model
    return genai.GenerativeModel('gemini-1.5-flash')

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. SIDEBAR INSTRUCTIONS & SETTINGS ---
with st.sidebar:
    st.markdown("## 🌐 Language Settings")
    # భాషను ఎంచుకోవడానికి డ్రాప్‌డౌన్
    selected_lang = st.selectbox(
        "Choose Output Language:",
        ["Telugu & English (Mix)", "Pure Telugu", "English Only", "Hindi"],
        index=0
    )
    
    st.divider()
    
    st.markdown("## 📖 Instructions")
    st.write("మీ యాత్ర వివరాలను టైప్ చేసి బటన్ నొక్కండి. నిమిషాల్లో ప్లాన్ సిద్ధమవుతుంది.")
    
    st.divider()
    
    st.markdown("## 🤖 AI Agents at Work")
    st.markdown("""
    <p><span class='agent-icon'>🗺️</span><b>Planner Agent:</b> రూట్ డిజైన్ చేస్తుంది.</p>
    <p><span class='agent-icon'>🔍</span><b>Researcher Agent:</b> ధరలు & సమయాలు వెతుకుతుంది.</p>
    <p><span class='agent-icon'>✍️</span><b>Writer Agent:</b> అందమైన గైడ్ రాస్తుంది.</p>
    """, unsafe_allow_html=True)
    
    st.divider()
    if st.button("Reset Everything"):
        st.session_state.itinerary_data = None
        st.rerun()

# --- 5. UI LAYOUT ---
st.markdown('<h1 class="header-text" style="font-size: 3.5rem;">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
# "Gemini 3 Edition" తొలగించబడింది
st.markdown('<p class="header-text" style="font-size: 1.3rem; margin-bottom: 30px;">మీ పర్సనల్ ట్రావెల్ ఏజెంట్</p>', unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    user_query = st.text_input("ప్రయాణ వివరాలు తెలపండి:", placeholder="ఉదా: 3 రోజుల అమరావతి యాత్ర ప్లాన్...")
    generate = st.button("Generate My Itinerary 🚀")

# --- 6. PROCESSING ---
if generate and user_query:
    model = get_gemini_model()
    if model:
        with st.status(f"ఏజెంట్లు పనిచేస్తున్నారు... ({selected_lang})", expanded=False) as status:
            # ఎంచుకున్న భాషను ప్రాంప్ట్‌కు జత చేయడం
            lang_instruction = f"The final response MUST be in {selected_lang}."
            
            st.write("🗺️ ప్లానర్ మార్గం వెతుకుతోంది...")
            plan = model.generate_content(f"Create a day-wise itinerary for {user_query}. {lang_instruction}").text
            
            st.write("🔍 రీసెర్చర్ ధరలు ధృవీకరిస్తోంది...")
            research = model.generate_content(f"Find entry fees and timings for: {plan}. {lang_instruction}").text
            
            st.write("✍️ రైటర్ ఫైనల్ గైడ్ రాస్తోంది...")
            final = model.generate_content(f"Create a high-quality guide with tables based on this: {research}. {lang_instruction}").text
            
            st.session_state.itinerary_data = final
            status.update(label="ప్లాన్ సిద్ధం! ✅", state="complete")

# --- 7. RESULTS ---
if st.session_state.itinerary_data:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.download_button("Download Full Guide 📥", st.session_state.itinerary_data, file_name="My_Travel_Plan.md")

st.markdown("<br><p style='text-align: center; color: white; opacity: 0.6;'>YatriMate AI © 2026</p>", unsafe_allow_html=True)

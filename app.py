import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - 2026 Premium", 
    page_icon="🗺️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED GUI (Image + Readability Overlay) ---
st.markdown("""
    <style>
    /* 1. Background Image with Dark Tint */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* 2. Global Text Colors */
    html, body, [class*="st-"], p, span, label {
        color: #1A1A1A !important; /* Deep Charcoal Black */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 3. Header Styling (White for Contrast against image) */
    .header-text {
        color: #FFFFFF !important;
        text-align: center;
        text-shadow: 2px 4px 8px rgba(0,0,0,0.7);
    }

    /* 4. Glassmorphism Card for Results */
    .itinerary-container {
        background: rgba(255, 255, 255, 0.96) !important; /* High opacity for text clarity */
        padding: 40px;
        border-radius: 20px;
        color: #1A1A1A !important;
        line-height: 1.8;
        font-size: 1.15rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-top: 6px solid #FF9933;
        margin-top: 30px;
    }

    /* 5. Input Box Area */
    .input-box-wrap {
        background: rgba(255, 255, 255, 0.85);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .stTextInput>div>div>input {
        background-color: white !important;
        color: #000000 !important;
        border: 2px solid #FF9933 !important;
        font-size: 1.1rem !important;
    }

    /* 6. Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF7700) !important;
        color: white !important;
        border: none !important;
        padding: 15px !important;
        font-weight: 800 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-radius: 10px !important;
        transition: 0.4s;
    }

    /* 7. Tables - High Contrast */
    table { background-color: white !important; color: black !important; }
    th { background-color: #f8f9fa !important; color: black !important; border: 1px solid #ddd !important; }
    td { border: 1px solid #eee !important; color: black !important; padding: 10px !important; }

    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ENGINE (Gemini 3 Flash) ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3-flash-preview')

# --- 4. SESSION STATE ---
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 5. UI LAYOUT ---
st.markdown('<h1 class="header-text" style="font-size: 4.5rem; margin-bottom:0;">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-text" style="font-size: 1.5rem; margin-bottom: 40px;">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ - 2026 Edition</p>', unsafe_allow_html=True)

# Main Input Section
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    st.markdown('<div class="input-box-wrap">', unsafe_allow_html=True)
    user_query = st.text_input("ప్రయాణ వివరాలు తెలపండి:", placeholder="ఉదా: 4 రోజుల కాశీ మరియు ప్రయాగరాజ్ యాత్ర ప్లాన్...")
    generate = st.button("Generate My Itinerary 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AGENT PIPELINE ---
if generate and user_query:
    model = get_gemini_model()
    if model:
        with st.status("ఏజెంట్లు మీ కోసం వెతుకుతున్నారు...", expanded=True) as status:
            # Multi-agent simulation
            st.write("🗺️ ప్లానర్: రూట్ మ్యాప్ తయారు చేస్తోంది...")
            p_res = model.generate_content(f"Day-wise skeleton for {user_query}")
            
            st.write("🔍 రీసెర్చర్: టికెట్ ధరలు మరియు సమయాలు సేకరిస్తోంది...")
            r_res = model.generate_content(f"Get entry fees and opening hours for: {p_res.text}")
            
            st.write("✍️ రైటర్: అందమైన టేబుల్స్ తో రిపోర్ట్ రాస్తోంది...")
            w_res = model.generate_content(f"Write a final travel guide in Telugu and English with tables. Data: {r_res.text}")
            
            st.session_state.itinerary_data = w_res.text
            status.update(label="యాత్ర ప్లాన్ సిద్ధంగా ఉంది! ✅", state="complete")

# --- 7. FINAL DISPLAY ---
if st.session_state.itinerary_data:
    st.markdown(f'<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download Button
    st.divider()
    st.download_button(
        label="Download Guide 📥",
        data=st.session_state.itinerary_data,
        file_name="YatriMate_Plan.md",
        mime="text/markdown"
    )

st.markdown("<br><p style='text-align: center; color: white; opacity: 0.7;'>Powered by Gemini 3 Flash Preview • 2026</p>", unsafe_allow_html=True)

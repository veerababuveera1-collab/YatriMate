import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Premium Edition", 
    page_icon="🚩", 
    layout="wide"
)

# --- 2. ADVANCED UI STYLING (No White Bars & High Contrast) ---
st.markdown("""
    <style>
    /* 1. Global Setup with High-Quality Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Remove Streamlit default white padding & bars */
    .block-container { padding-top: 1.5rem !important; }
    header, footer { visibility: hidden; }
    
    /* 2. Typography */
    h1, h2, h3, p, span, li, label {
        font-family: 'Poppins', sans-serif !important;
        color: white !important;
    }

    /* 3. Glassmorphism Card Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 32px rgba(0,0,0,0.5);
        height: 100%;
    }

    /* 4. Result Itinerary Card - Pure White for Readability */
    .result-card {
        background: #FFFFFF !important;
        color: #1A1A1A !important;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        border-top: 10px solid #FF9933;
    }
    .result-card p, .result-card h1, .result-card h2, .result-card h3, .result-card td, .result-card li {
        color: #1A1A1A !important;
    }

    /* 5. Professional Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #FF5500 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-weight: 700 !important;
        width: 100%;
        transition: 0.3s ease;
        font-size: 1.1rem !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 85, 0, 0.5);
    }
    
    /* Input Box Styling */
    .stTextInput input {
        background-color: rgba(255,255,255,0.95) !important;
        color: black !important;
        border-radius: 12px !important;
        height: 55px !important;
        font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI ENGINE SETUP ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("API Key missing! Please add it to your secrets.")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3-flash-preview')

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. HEADER SECTION ---
st.markdown("<h1 style='text-align: center; font-size: 4.5rem; margin-bottom: 0;'>🚩 YatriMate AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.4rem; opacity: 0.8;'>Your Ultimate Travel Planning Partner • 2026</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- 5. TOP CARDS (Instructions & Settings) ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div class="glass-card">
        <h3 style='margin-top:0; text-align: center;'>📖 How to Use</h3>
        <p>• <b>Step 1:</b> Enter your destination (e.g., 3 days Vizag trip).</p>
        <p>• <b>Step 2:</b> Choose your preferred language in settings.</p>
        <p>• <b>Step 3:</b> Hit 'Plan My Trip' and get your guide instantly!</p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; text-align: center;'>🌐 Settings</h3>", unsafe_allow_html=True)
    
    # Language selection and Reset side-by-side
    l_col, r_col = st.columns([2, 1])
    with l_col:
        selected_lang = st.selectbox("Language:", ["Telugu & English Mix", "Pure Telugu", "English", "Hindi"], label_visibility="collapsed")
    with r_col:
        if st.button("Reset App"):
            st.session_state.itinerary_data = None
            st.rerun()
    st.markdown("<p style='text-align: center; font-size: 0.9rem; margin-top: 10px; opacity: 0.7;'>Note: Plan will be generated in chosen language.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. INPUT SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
col_l, col_m, col_r = st.columns([1, 4, 1])
with col_m:
    user_input = st.text_input("Destination Details:", placeholder="Ex: 4 days pilgrimage trip to Kashi and Ayodhya...")
    if st.button("Plan My Trip 🚀"):
        if user_input:
            model = get_gemini_model()
            if model:
                with st.status("Coordinating AI Agents...", expanded=False) as status:
                    # Multi-agent simulation via prompt engineering
                    st.write("🗺️ Planner: Mapping out the best route...")
                    plan_skeleton = model.generate_content(f"Create a day-wise route for {user_input}").text
                    
                    st.write("🔍 Researcher: Checking entry fees and timings...")
                    research_data = model.generate_content(f"Verify fees and opening hours for: {plan_skeleton}").text
                    
                    st.write("✍️ Writer: Crafting your personalized guide...")
                    final_itinerary = model.generate_content(f"Write a detailed travel guide with tables in {selected_lang} based on: {research_data}").text
                    
                    st.session_state.itinerary_data = final_itinerary
                    status.update(label="Itinerary Successfully Created! ✅", state="complete")
        else:
            st.warning("Please enter a destination first!")

# --- 7. RESULTS DISPLAY ---
if st.session_state.itinerary_data:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col_res, col_r = st.columns([1, 8, 1])
    with col_res:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(st.session_state.itinerary_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Section
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Download Detailed Plan 📥",
            data=st.session_state.itinerary_data,
            file_name="YatriMate_Travel_Plan.md",
            mime="text/markdown"
        )

st.markdown("<br><p style='text-align: center; color: white; opacity: 0.5;'>YatriMate AI © 2026 | Powered by Gemini 3 Flash</p>", unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Edition", 
    page_icon="🚩", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. HIGH-CONTRAST CLEAN UI (White & Black) ---
st.markdown("""
    <style>
    /* Force Light Mode Aesthetics */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Global Text Color - Deep Charcoal for readability */
    html, body, [class*="st-"], div, p, span, label {
        color: #1A1A1A !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Titles */
    h1, h2, h3 {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* Input Field */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #DDDDDD !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }

    /* Results Container - Pure White with subtle shadow */
    .itinerary-container {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #EEEEEE;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        line-height: 1.8;
        font-size: 1.1rem;
    }

    /* Increase Telugu Font Size Specifically */
    .telugu-text {
        font-size: 1.25rem;
        line-height: 2;
    }

    /* Tables Styling - High Contrast */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    th {
        background-color: #F2F2F2 !important;
        color: #000000 !important;
        font-weight: bold;
        border: 1px solid #CCCCCC !important;
        padding: 12px !important;
    }
    td {
        border: 1px solid #EEEEEE !important;
        padding: 12px !important;
    }

    /* Action Button - Saffron Gradient */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF7700) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        width: 100%;
    }
    
    /* Horizontal Rule */
    hr {
        border: 0;
        border-top: 1px solid #EEEEEE !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ENGINE (Gemini 3 Flash) ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("API Key missing! Please add it to Streamlit Secrets.")
        return None
    genai.configure(api_key=api_key)
    # Using the latest Gemini 3 model for 2026
    return genai.GenerativeModel('gemini-3-flash-preview')

def agent_call(model, prompt, role_desc):
    full_prompt = f"Role: {role_desc}. Language: Mix of Telugu and English. Output should be clear and professional.\n\nTask: {prompt}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. SESSION STATE ---
if 'final_guide' not in st.session_state:
    st.session_state.final_guide = None

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🚩 YatriMate AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555 !important;'>మీ పర్సనల్ ట్రావెల్ ఏజెంట్ - Gemini 3 Edition</p>", unsafe_allow_html=True)
st.markdown("---")

# Centered Input Box
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    user_query = st.text_input("ప్రయాణ వివరాలు తెలపండి:", placeholder="ఉదా: 3 రోజుల అమరావతి యాత్ర ప్లాన్...")
    submit = st.button("Generate My Itinerary")

# --- 6. PROCESSING WORKFLOW ---
if submit and user_query:
    model = get_gemini_model()
    if model:
        with st.status("ఏజెంట్లు పనిచేస్తున్నారు...", expanded=True) as status:
            st.write("🗺️ ప్లానర్: రూట్ సిద్ధం చేస్తోంది...")
            plan = agent_call(model, f"Create a logical day-wise skeleton for {user_query}", "Travel Architect")
            
            st.write("🔍 రీసెర్చర్: ధరలు మరియు సమయాలు ధృవీకరిస్తోంది...")
            research = agent_call(model, f"Provide current entry fees and timings for these places: {plan}", "Fact Checker")
            
            st.write("✍️ రైటర్: ఫైనల్ గైడ్ రాస్తోంది...")
            final = agent_call(model, f"Create a detailed travel guide with tables in Telugu and English. Use this data: {research}", "Professional Travel Writer")
            
            st.session_state.final_guide = final
            status.update(label="యాత్ర ప్లాన్ సిద్ధంగా ఉంది! ✅", state="complete", expanded=False)

# --- 7. DISPLAY RESULTS ---
if st.session_state.final_guide:
    st.markdown("### 📔 మీ ప్రత్యేక ప్రయాణ నివేదిక")
    
    # Render final output in the clean container
    st.markdown(f'<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.final_guide)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Download and Reset
    d_col1, d_col2 = st.columns([1, 1])
    with d_col1:
        st.download_button("Download Plan (MD) 📥", st.session_state.final_guide, file_name="My_Travel_Plan.md")
    with d_col2:
        if st.button("Reset & Start New"):
            st.session_state.final_guide = None
            st.rerun()

# --- 8. FOOTER ---
st.markdown("<br><p style='text-align: center; font-size: 0.8rem; color: #888 !important;'>YatriMate AI © 2026 | Smart Multi-Agent System</p>", unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Premium Cards", 
    page_icon="🚩", 
    layout="wide"
)

# --- 2. PREMIUM CARD STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                    url("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=2000&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Titles */
    .header-text {
        color: #FFFFFF !important;
        text-align: center;
        text-shadow: 2px 2px 15px rgba(0,0,0,1);
        font-weight: 800;
    }

    /* Card Styling */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        color: #1A1A1A !important;
        height: 100%;
        border-top: 5px solid #FF9933;
        transition: 0.3s;
    }
    .info-card:hover {
        transform: translateY(-5px);
    }

    /* Input Card */
    .input-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        margin-top: 20px;
    }

    /* Result Itinerary Card */
    .itinerary-container {
        background: #FFFFFF !important; 
        padding: 40px;
        border-radius: 20px;
        color: #000000 !important;
        line-height: 1.8;
        font-size: 1.15rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        border-left: 10px solid #FF9933;
    }

    /* Agent Animation */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    .agent-icon {
        display: inline-block;
        animation: bounce 1.5s infinite;
        font-size: 1.8rem;
    }

    /* Labels & Text */
    label, p, li { color: #1A1A1A !important; font-weight: 500; }
    
    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF7700) !important;
        color: white !important;
        font-weight: bold !important;
        height: 55px;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 153, 51, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE ENGINE ---
def get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("API Key missing! Check Secrets.")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3-flash-preview')

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. TOP SECTION (Header) ---
st.markdown('<h1 class="header-text" style="font-size: 3.5rem; margin-top: -30px;">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-text" style="font-size: 1.3rem; margin-bottom: 30px;">Your Smart Multi-Agent Travel Engine</p>', unsafe_allow_html=True)

# --- 5. INFO CARDS SECTION ---
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="info-card">
        <h3>📖 Instructions</h3>
        <ul>
            <li>Enter your dream destination.</li>
            <li>Select your preferred language.</li>
            <li>Get a detailed plan in seconds!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-card" style="text-align: center;">
        <h3>🤖 AI Agents</h3>
        <p><span class="agent-icon">🗺️</span> <b>Planner</b></p>
        <p><span class="agent-icon">🔍</span> <b>Researcher</b></p>
        <p><span class="agent-icon">✍️</span> <b>Writer</b></p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("<h3>🌐 Language</h3>")
    selected_lang = st.selectbox("Choose Output Language:", 
                                ["Telugu & English (Mix)", "Pure Telugu", "English Only", "Hindi"],
                                label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset App"):
        st.session_state.itinerary_data = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. INPUT SECTION ---
st.markdown('<div class="input-card">', unsafe_allow_html=True)
user_query = st.text_input("Where do you want to go? (మీ ప్రయాణ గమ్యం):", placeholder="Ex: 5 days trip to Kashi and Ayodhya...")
generate = st.button("Plan My Trip 🚀")
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. AGENT LOGIC ---
if generate and user_query:
    model = get_gemini_model()
    if model:
        with st.status(f"Agents are coordinating in {selected_lang}...", expanded=False) as status:
            lang_prompt = f"The final response MUST be in {selected_lang}."
            
            st.write("🗺️ Planner is mapping the route...")
            plan = model.generate_content(f"Day-wise itinerary skeleton for {user_query}. {lang_prompt}").text
            
            st.write("🔍 Researcher is checking timings/fees...")
            research = model.generate_content(f"Verify entry fees and hours for: {plan}. {lang_prompt}").text
            
            st.write("✍️ Writer is crafting the guide...")
            final = model.generate_content(f"Create a professional travel guide with tables using: {research}. {lang_prompt}").text
            
            st.session_state.itinerary_data = final
            status.update(label="Itinerary Ready! ✅", state="complete")

# --- 8. RESULTS DISPLAY ---
if st.session_state.itinerary_data:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="itinerary-container">', unsafe_allow_html=True)
    st.markdown(st.session_state.itinerary_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("Download Full Itinerary 📥", st.session_state.itinerary_data, file_name="YatriMate_Itinerary.md")

st.markdown("<br><p style='text-align: center; color: white; opacity: 0.6;'>YatriMate AI © 2026 | Powered by Gemini 3 Flash</p>", unsafe_allow_html=True)

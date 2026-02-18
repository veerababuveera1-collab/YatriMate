import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Premium Agent Planner",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MULTI-AGENT ENGINE ---
def run_travel_agents(query, lang):
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key: return "Setup Error: Google API Key missing."
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Agent Personas & Task (Multi-Agent Prompting)
        agent_prompt = f"""
        Act as a professional Multi-Agent Travel System for the destination: {query}.
        
        1. Agent 'Itinerary Specialist': Create a logical day-wise travel plan.
        2. Agent 'Budget Analyst': Provide an estimated cost breakdown (Flights, Stay, Food) in INR.
        3. Agent 'Local Expert': Suggest 3 local dishes to try and 2 'Hidden Gems' (off-beat places).
        
        Language: {lang}.
        Formatting: Use clear Markdown headers for each Agent's report.
        """
        
        response = model.generate_content(agent_prompt)
        return response.text
    except Exception as e:
        return f"Agent Logic Error: {str(e)}"

# --- 3. UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.85)), 
                    url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2073");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 4rem !important;
        font-weight: 900;
        text-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 600;
        letter-spacing: 2px;
        margin-bottom: 40px;
    }
    
    .agent-box {
        background: rgba(255, 255, 255, 0.98);
        color: #1a1a1a;
        padding: 40px;
        border-radius: 30px;
        border-left: 15px solid #FF9933;
        box-shadow: 0 40px 100px rgba(0,0,0,0.5);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP STATE ---
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 5. HERO SECTION ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Powered by 3 Smart AI Agents</p>', unsafe_allow_html=True)

# --- 6. SEARCH AREA ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (e.g. 5 days trip to Goa...)")
    generate = st.button("Activate Agents 🚀", use_container_width=True)

# --- 7. AGENT EXECUTION ---
if generate and user_query:
    with st.status("🤖 Calling AI Agents...", expanded=True) as status:
        st.write("🕵️ Itinerary Specialist is working...")
        st.write("💰 Budget Analyst is calculating...")
        st.write("🥘 Local Expert is gathering food tips...")
        
        result = run_travel_agents(user_query, "Telugu & English Mix")
        st.session_state.itinerary_data = result
        status.update(label="Planning Complete!", state="complete", expanded=False)
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div class="agent-box">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)
    if st.button("Clear Plan 🔄"):
        st.session_state.itinerary_data = None
        st.rerun()

# --- 8. FOOTER ---
st.markdown(f"""
    <div style="background: rgba(0, 0, 0, 0.7); padding: 50px; border-radius: 35px; margin-top: 100px; color: white; text-align: center;">
        <h2 style="color:#FF9933;">🚩 Yatri Mate AI</h2>
        <p>మీ నమ్మకమైన Multi-Agent ట్రావెల్ ప్లానర్.</p>
        <p>© 2026 All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)

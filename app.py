import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM & PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Multi-Agent Planner",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. MULTI-AGENT LOGIC ---
def run_travel_agents(query):
    try:
        # Streamlit Secrets నుండి API కీ ని తీసుకుంటుంది
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Multi-Agent Role Assignment (ముగ్గురు ఏజెంట్ల బాధ్యతలు)
        prompt = f"""
        Act as a professional Multi-Agent Travel System for the destination: {query}.
        
        1. Agent 'Itinerary': Design a logical day-wise travel plan.
        2. Agent 'Budget': Provide an estimated cost breakdown in INR for middle-class travelers.
        3. Agent 'Guide': List top 3 local foods to try and 2 hidden gems (less crowded places).
        
        Output Language: Mix of Telugu and English.
        Formatting: Use Markdown with clear headings for each Agent's report.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: API Key missing or Agent failed. Details: {str(e)}"

# --- 3. PREMIUM UI STYLING (Mind-blowing & Clean) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)), 
                    url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2073");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .main-title {
        color: white;
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        margin-bottom: 0px;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .sub-title {
        color: #FF9933;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 40px;
    }

    /* Result Glassmorphism */
    .agent-result-container {
        background: rgba(255, 255, 255, 0.95);
        color: #1a1a1a;
        padding: 40px;
        border-radius: 25px;
        border-left: 15px solid #FF9933;
        box-shadow: 0 30px 60px rgba(0,0,0,0.4);
        margin-top: 20px;
        line-height: 1.7;
    }

    /* Input Box Styling */
    .stTextInput input {
        border-radius: 15px !important;
        height: 55px !important;
        font-size: 1.1rem !important;
    }
    
    /* Destination Cards */
    .dest-card {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 153, 51, 0.3);
        border-radius: 20px;
        padding: 10px;
        transition: 0.3s;
        text-align: center;
    }
    .dest-card:hover { transform: translateY(-10px); border-color: #FF9933; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP INTERFACE ---

# Header
st.markdown('<h1 class="main-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Powered by 3 Specialized AI Agents</p>', unsafe_allow_html=True)

# Session State for storing data
if 'agent_report' not in st.session_state:
    st.session_state.agent_report = None

# Search Section
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (e.g., 4 days in Bali)")
    if st.button("Activate Agents 🚀", use_container_width=True):
        if query:
            with st.status("🤖 Multi-Agent System Processing...", expanded=True) as status:
                st.write("🕵️ Agent 'Itinerary' is drafting the route...")
                st.write("💰 Agent 'Budget' is calculating expenses...")
                st.write("🥘 Agent 'Guide' is picking local flavors...")
                
                result = run_travel_agents(query)
                st.session_state.agent_report = result
                status.update(label="Planning Complete!", state="complete", expanded=False)
                st.rerun()
        else:
            st.warning("Please enter a destination first!")

# Display Results
if st.session_state.agent_report:
    st.markdown(f'<div class="agent-result-container">{st.session_state.agent_report}</div>', unsafe_allow_html=True)
    if st.button("Plan Another Trip 🔄"):
        st.session_state.agent_report = None
        st.rerun()

# --- 5. TRENDING SECTION (Show only if no result) ---
if not st.session_state.agent_report:
    st.markdown("<br><h3 style='text-align:center; color:white;'>📍 Trending Destinations</h3>", unsafe_allow_html=True)
    d_cols = st.columns(4)
    trending = [
        {"n": "Maldives", "u": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=300"},
        {"n": "Switzerland", "u": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=300"},
        {"n": "Manali", "u": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=300"},
        {"n": "Paris", "u": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300"}
    ]
    for i, d in enumerate(trending):
        with d_cols[i]:
            st.markdown(f"""
                <div class="dest-card">
                    <img src="{d['u']}" style="width:100%; border-radius:15px;">
                    <p style="color:white; font-weight:bold; margin-top:10px;">{d['n']}</p>
                </div>
            """, unsafe_allow_html=True)

# --- 6. FOOTER ---
st.markdown(f"""
    <div style="text-align:center; color:rgba(255,255,255,0.5); padding:50px; margin-top:50px; border-top:1px solid rgba(255,255,255,0.1);">
        <p>© 2026 YatriMate AI • Multi-Agent Travel Intelligence</p>
        <p>📍 Saidabad, Hyderabad | 📞 +91-6304001323</p>
    </div>
""", unsafe_allow_html=True)

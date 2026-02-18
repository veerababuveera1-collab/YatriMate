import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Multi-Agent Engine",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. MULTI-AGENT AI LOGIC ---
def run_travel_agent_system(query, lang):
    try:
        # Streamlit Secrets నుండి మీ పాత API Key ని తీసుకుంటుంది
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Multi-Agent Persona Logic
        prompt = f"""
        You are a Multi-Agent Travel Intelligence System for: {query}.
        Provide the response in 3 distinct sections:

        1. 🕵️ Agent 'Route Architect': Suggest 2-3 mandatory 'Middle Destination' stopovers between the source and final destination. Explain their importance.
        2. 📅 Agent 'Itinerary Planner': Create a professional day-wise schedule including those middle stops.
        3. 💰 Agent 'Budget & Food Expert': Give an estimated budget in INR and suggest 3 local dishes to try.

        Language: {lang}.
        Formatting: Use professional Markdown with bold headers, icons, and bullet points.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: API Key missing or expired. Details: {str(e)}"

# --- 3. PREMIUM UI STYLING (GUI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                    url("https://images.unsplash.com/photo-1503220317375-aaad61436b1b?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    
    .hero-title {
        color: white !important; text-align: center; font-size: 4rem !important; 
        font-weight: 900; text-shadow: 0 10px 25px rgba(0,0,0,0.8); margin-bottom: 0px;
    }
    
    .sub-title {
        color: #FF9933 !important; text-align: center; font-size: 1.3rem; 
        font-weight: bold; margin-bottom: 40px;
    }

    /* GUI Place Cards Styling */
    .img-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px; overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.4s ease; text-align: center;
    }
    .img-card:hover {
        transform: translateY(-10px);
        border-color: #FF9933;
        box-shadow: 0 20px 40px rgba(255, 153, 51, 0.3);
    }
    .dest-img { width: 100%; height: 200px; object-fit: cover; }
    .dest-label { padding: 15px; color: white; font-weight: bold; background: rgba(0,0,0,0.6); }

    /* Results Card */
    .itinerary-container {
        background: white; color: #1a1a1a; padding: 45px; 
        border-radius: 30px; border-left: 15px solid #FF9933;
        box-shadow: 0 30px 60px rgba(0,0,0,0.6); margin-top: 30px;
    }

    /* Custom Button */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important; border-radius: 12px !important;
        height: 55px; font-weight: bold; font-size: 1.1rem; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HERO SECTION ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Multi-Agent Intelligence for Perfect Journeys</p>', unsafe_allow_html=True)

if 'final_plan' not in st.session_state:
    st.session_state.final_plan = None

# Search Logic
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="Enter Route (e.g., Hyderabad to Varanasi via Nagpur)...", label_visibility="collapsed")
    if st.button("Activate Agents 🚀", use_container_width=True):
        if user_query:
            with st.status("🤖 Coordinating AI Agents...", expanded=True) as status:
                st.write("🕵️ Route Architect is mapping middle destinations...")
                st.write("📅 Itinerary Planner is scheduling your trip...")
                st.write("💰 Budget Specialist is calculating costs...")
                
                result = run_travel_agent_system(user_query, "Telugu & English Mix")
                st.session_state.final_plan = result
                status.update(label="Planning Complete!", state="complete")
                st.rerun()

# --- 5. DISPLAY RESULTS OR TRENDING CARDS ---
if st.session_state.final_plan:
    st.markdown(f'<div class="itinerary-container">{st.session_state.final_plan}</div>', unsafe_allow_html=True)
    if st.button("🔄 Plan New Trip"):
        st.session_state.final_plan = None
        st.rerun()
else:
    # --- TRENDING PLACES CARDS (GUI) ---
    st.markdown("<h3 style='text-align: center; color: white; margin-top: 40px;'>📍 Trending Destinations</h3>", unsafe_allow_html=True)
    
    trending = [
        {"name": "Araku Valley", "url": "https://images.unsplash.com/photo-1623945417534-1907797709b1?w=400"},
        {"name": "Tirumala Temple", "url": "https://images.unsplash.com/photo-1594913217002-869272825126?w=400"},
        {"name": "Kerala Backwaters", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400"},
        {"name": "Varanasi Ghats", "url": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"}
    ]
    
    cols = st.columns(4)
    for i, d in enumerate(trending):
        with cols[i]:
            st.markdown(f"""
                <div class="img-card">
                    <img src="{d['url']}" class="dest-img">
                    <div class="dest-label">{d['name']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. PROFESSIONAL FOOTER ---
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 50px; border-radius: 30px; margin-top: 100px; border-top: 1px solid #FF9933;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px;">
            <div style="flex: 2; min-width: 300px;">
                <h2 style="color:#FF9933;">🚩 YatriMate AI</h2>
                <p style="color:white; opacity: 0.8;">మీ ప్రయాణాన్ని అత్యంత సులభంగా మరియు ప్రొఫెషనల్‌గా ప్లాన్ చేసే ఏకైక AI వేదిక. 
                ముగ్గురు స్పెషలిస్ట్ ఏజెంట్లు మీ కోసం 24/7 అందుబాటులో ఉంటారు.</p>
            </div>
            <div style="flex: 1; min-width: 250px; color:white;">
                <h4>📍 Reach Us</h4>
                <p>Saidabad Main Road, Hyderabad, 500059<br>
                <b>Mobile:</b> +91-6304001323<br>
                <b>Email:</b> veerababu.veera1@gmail.com</p>
            </div>
        </div>
        <p style='text-align: center; color: gray; font-size: 0.9rem; margin-top: 40px;'>© 2026 YatriMate AI | Multi-Agent Route Intelligence v4.0</p>
    </div>
""", unsafe_allow_html=True)

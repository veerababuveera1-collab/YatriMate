import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Multi-Agent Travel Planner",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. MULTI-AGENT ENGINE LOGIC ---
def run_travel_agent_system(query, lang):
    try:
        # Streamlit Secrets నుండి API Key ని తీసుకుంటుంది
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Multi-Agent Role Assignment
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Your output must be structured from these 3 specialized AI Agents:

        1. 🕵️ Agent 'Route Architect': Identify 2-3 mandatory 'Middle Destination' stops between the starting point and final destination. Explain why they are worth visiting.
        2. 📅 Agent 'Itinerary Planner': Create a logical day-wise travel schedule that includes these middle stops.
        3. 💰 Agent 'Budget & Local Expert': Provide a middle-class budget estimate in INR and list 3 must-try local foods.

        Output Language: {lang}.
        Formatting: Use professional Markdown with bold headers, icons, and clean lists.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ API Error: Please check if GOOGLE_API_KEY is set in Secrets. Error: {str(e)}"

# --- 3. PREMIUM GUI STYLING ---
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

    /* Destination Card GUI */
    .img-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px; overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.4s ease; text-align: center;
        margin-bottom: 25px;
    }
    .img-card:hover {
        transform: translateY(-10px);
        border-color: #FF9933;
        box-shadow: 0 20px 40px rgba(255, 153, 51, 0.3);
    }
    .dest-img { width: 100%; height: 180px; object-fit: cover; }
    .dest-label { padding: 12px; color: white; font-weight: bold; background: rgba(0,0,0,0.6); }

    /* Results Card */
    .report-box {
        background: white; color: #1a1a1a; padding: 45px; 
        border-radius: 30px; border-left: 15px solid #FF9933;
        box-shadow: 0 30px 60px rgba(0,0,0,0.6); margin-top: 30px;
    }

    /* Action Button */
    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important; border-radius: 12px !important;
        height: 55px; font-weight: bold; font-size: 1.1rem; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER SECTION ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Multi-Agent Intelligence for Smart Road Trips</p>', unsafe_allow_html=True)

if 'plan_output' not in st.session_state:
    st.session_state.plan_output = None

# Search Logic
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="Enter Route (e.g., Hyderabad to Goa via Hampi)...", label_visibility="collapsed")
    if st.button("Activate AI Agents 🚀", use_container_width=True):
        if user_query:
            with st.status("🤖 Coordinating Agents...", expanded=True) as status:
                st.write("🕵️ Route Architect is finding stopovers...")
                st.write("📅 Itinerary Planner is mapping your days...")
                st.write("💰 Budget Specialist is calculating INR...")
                
                result = run_travel_agent_system(user_query, "Telugu & English Mix")
                st.session_state.plan_output = result
                status.update(label="Full Plan Ready!", state="complete")
                st.rerun()

# --- 5. DISPLAY RESULTS OR CARDS ---
if st.session_state.plan_output:
    st.markdown(f'<div class="report-box">{st.session_state.plan_output}</div>', unsafe_allow_html=True)
    if st.button("🔄 Plan Another Journey"):
        st.session_state.plan_output = None
        st.rerun()
else:
    # --- 2 LINES OF DESTINATION CARDS ---
    
    # LINE 1: INTERNATIONAL
    st.markdown("<h3 style='color: white; margin-top: 20px;'>🌍 International Destinations</h3>", unsafe_allow_html=True)
    intl = [
        {"name": "Paris, France", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"},
        {"name": "Dubai, UAE", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400"},
        {"name": "Bali, Indonesia", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400"},
        {"name": "Switzerland", "url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=400"}
    ]
    cols1 = st.columns(4)
    for i, d in enumerate(intl):
        with cols1[i]:
            st.markdown(f'<div class="img-card"><img src="{d["url"]}" class="dest-img"><div class="dest-label">{d["name"]}</div></div>', unsafe_allow_html=True)

    # LINE 2: LOCAL / INDIAN
    st.markdown("<h3 style='color: white; margin-top: 10px;'>🏞️ Local Treasures</h3>", unsafe_allow_html=True)
    local = [
        {"name": "Kerala Backwaters", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400"},
        {"name": "Ladakh, India", "url": "https://images.unsplash.com/photo-1581791538302-03537b9c97bf?w=400"},
        {"name": "Hampi, Karnataka", "url": "https://images.unsplash.com/photo-1581335031104-5415758f1422?w=400"},
        {"name": "Goa Beaches", "url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400"}
    ]
    cols2 = st.columns(4)
    for i, d in enumerate(local):
        with cols2[i]:
            st.markdown(f'<div class="img-card"><img src="{d["url"]}" class="dest-img"><div class="dest-label">{d["name"]}</div></div>', unsafe_allow_html=True)

# --- 6. FOOTER SECTION ---
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 50px; border-radius: 30px; margin-top: 100px; border-top: 1px solid #FF9933;">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px;">
            <div style="flex: 2; min-width: 300px;">
                <h2 style="color:#FF9933;">🚩 YatriMate AI</h2>
                <p style="color:white; opacity: 0.8;">మీ ప్రయాణాన్ని అత్యంత సులభంగా మరియు ప్రొఫెషనల్‌గా ప్లాన్ చేసే ఏకైక AI వేదిక. ముగ్గురు ఏజెంట్లు మీ సేవలో ఉంటారు.</p>
            </div>
            <div style="flex: 1; min-width: 250px; color:white;">
                <h4>📍 Reach Us</h4>
                <p>Saidabad Main Road, Hyderabad, 500059<br>
                <b>Mobile:</b> +91-6304001323<br>
                <b>Email:</b> veerababu.veera1@gmail.com</p>
            </div>
        </div>
        <p style='text-align: center; color: gray; font-size: 0.9rem; margin-top: 40px;'>© 2026 YatriMate AI | Multi-Agent Intelligence v5.0</p>
    </div>
""", unsafe_allow_html=True)

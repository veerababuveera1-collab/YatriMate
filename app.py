import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Premium Agent Planner",
    page_icon="🚩",
    layout="wide"
)

# --- 2. MULTI-AGENT AI ENGINE ---
def run_agents(query):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a 3-Agent Travel Team for: {query}.
        1. Agent 'Route Specialist': Identify 2-3 middle destinations (stopovers) between source and main destination.
        2. Agent 'Budget Master': Breakdown the cost in INR for travel, food, and stay.
        3. Agent 'Local Guide': Suggest top food items and hidden gems at each stop.
        
        Format the response in a professional Mix of Telugu & English with clear headings.
        """
        response = model.generate_content(prompt)
        return response.text
    except:
        return "⚠️ API Key not found. Please add GOOGLE_API_KEY in Streamlit Secrets."

# --- 3. CUSTOM CSS FOR GUI & CARDS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=2074");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Hero Title */
    .hero-title {
        color: white; text-align: center; font-size: 4rem; font-weight: 900;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 0px;
    }
    
    /* Destination Cards */
    .dest-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        transition: 0.4s;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    .dest-card:hover {
        transform: translateY(-10px);
        border-color: #FF9933;
        background: rgba(255, 153, 51, 0.1);
    }
    .dest-img {
        width: 100%; height: 180px; object-fit: cover; border-radius: 15px;
    }
    .dest-name {
        color: white; font-weight: bold; font-size: 1.2rem; margin-top: 10px;
    }

    /* Result Box */
    .result-box {
        background: white; color: #1a1a1a; padding: 40px; 
        border-radius: 25px; border-left: 15px solid #FF9933;
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. APP INTERFACE ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#FF9933; text-align:center; font-weight:bold; letter-spacing:2px;">MULTI-AGENT ROUTE INTELLIGENCE</p>', unsafe_allow_html=True)

if 'plan' not in st.session_state:
    st.session_state.plan = None

# Search Section
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    query = st.text_input("", placeholder="Enter Route (e.g., Hyderabad to Manali road trip)")
    if st.button("Activate Agents 🚀", use_container_width=True):
        if query:
            with st.status("🤖 Agents are coordinating your trip...", expanded=True) as status:
                st.write("🕵️ Route Architect is finding middle stops...")
                st.write("💰 Budget Specialist is calculating costs...")
                st.write("🥘 Local Guide is picking food...")
                st.session_state.plan = run_agents(query)
                status.update(label="Planning Complete!", state="complete")
                st.rerun()

# --- 5. TRENDING CARDS SECTION (Only shows if no plan is generated) ---
if not st.session_state.plan:
    st.markdown("<h3 style='color:white; text-align:center; margin-top:40px;'>📍 Trending Destinations</h3>", unsafe_allow_html=True)
    
    # 3-Agent Workflow visualization context
    
    
    dests = [
        {"name": "Bali", "img": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400"},
        {"name": "Switzerland", "img": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=400"},
        {"name": "Varanasi", "img": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"},
        {"name": "Maldives", "img": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400"}
    ]
    
    cols = st.columns(4)
    for i, d in enumerate(dests):
        with cols[i]:
            st.markdown(f"""
                <div class="dest-card">
                    <img src="{d['img']}" class="dest-img">
                    <div class="dest-name">{d['name']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. DISPLAY AI RESULT ---
if st.session_state.plan:
    st.markdown(f'<div class="result-box">{st.session_state.plan}</div>', unsafe_allow_html=True)
    if st.button("Plan a New Journey 🔄"):
        st.session_state.plan = None
        st.rerun()

# --- 7. FOOTER ---
st.markdown(f"""
    <div style="text-align:center; color:gray; padding:40px; margin-top:50px; border-top:1px solid rgba(255,255,255,0.1);">
        <p>© 2026 YatriMate AI • Agent Intelligence v3.5</p>
        <p>Saidabad, Hyderabad | +91-6304001323</p>
    </div>
""", unsafe_allow_html=True)

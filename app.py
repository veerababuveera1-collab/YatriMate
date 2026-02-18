import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Multi-Agent Engine",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. MULTI-AGENT ENGINE LOGIC (FIXED MODEL CALL) ---
def run_travel_agent_system(query, lang):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # మోడల్ పేరును 'gemini-1.5-flash' గా లేదా 'gemini-1.5-flash-latest' గా ప్రయత్నించండి
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional Multi-Agent Travel System for: {query}.
        Structure the response using these 3 specialized AI Agents:

        1. 🕵️ Agent 'Route Architect': Identify 2-3 mandatory 'Middle Destination' stops (stopovers) between the source and final destination. Explain why they are worth visiting.
        2. 📅 Agent 'Itinerary Planner': Create a detailed day-wise schedule including those middle stops.
        3. 💰 Agent 'Budget & Food Expert': Give a middle-class budget estimate in INR and list 3 must-try local dishes.

        Output Language: {lang}.
        Formatting: Use professional Markdown with bold headers, icons, and bullet points.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # ఎర్రర్ మెసేజ్ మరింత క్లియర్ గా ఉండేలా మార్పు
        return f"⚠️ AI Error: {str(e)}. Please ensure your API Key is valid and Billing is enabled if required."

# --- 3. PREMIUM GUI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                    url("https://images.unsplash.com/photo-1503220317375-aaad61436b1b?q=80&w=2070");
        background-size: cover; background-attachment: fixed;
    }
    .hero-title { color: white !important; text-align: center; font-size: 4rem !important; font-weight: 900; }
    .sub-title { color: #FF9933 !important; text-align: center; font-size: 1.3rem; font-weight: bold; margin-bottom: 40px; }
    .img-card {
        background: rgba(255, 255, 255, 0.08); border-radius: 20px; overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2); transition: 0.4s ease; text-align: center; margin-bottom: 25px;
    }
    .img-card:hover { transform: translateY(-10px); border-color: #FF9933; box-shadow: 0 20px 40px rgba(255, 153, 51, 0.3); }
    .dest-img { width: 100%; height: 180px; object-fit: cover; }
    .dest-label { padding: 12px; color: white; font-weight: bold; background: rgba(0,0,0,0.6); }
    .itinerary-box { background: white; color: #1a1a1a; padding: 45px; border-radius: 30px; border-left: 15px solid #FF9933; margin-top: 30px; }
    div.stButton > button { background: linear-gradient(90deg, #FF9933, #FF5500) !important; color: white !important; border-radius: 12px; height: 55px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER & INPUT ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Smart Multi-Agent Intelligence for Global & Local Journeys</p>', unsafe_allow_html=True)

if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    query = st.text_input("", placeholder="Enter Route (e.g., Hyderabad to Varanasi via Nagpur)...", label_visibility="collapsed")
    if st.button("Activate Agents 🚀"):
        if query:
            with st.status("🤖 AI Agents Coordinating...", expanded=True) as status:
                st.write("🕵️ Finding middle stops & scheduling...")
                result = run_travel_agent_system(query, "Telugu & English Mix")
                st.session_state.itinerary = result
                status.update(label="Planning Complete!", state="complete")
                st.rerun()

# --- 5. DISPLAY RESULTS OR CARDS ---
if st.session_state.itinerary:
    st.markdown(f'<div class="itinerary-box">{st.session_state.itinerary}</div>', unsafe_allow_html=True)
    if st.button("🔄 Plan Another Trip"):
        st.session_state.itinerary = None
        st.rerun()
else:
    # ROW 1: INTERNATIONAL
    st.markdown("<h3 style='color: white; margin-top: 20px;'>🌍 International Getaways</h3>", unsafe_allow_html=True)
    intl_dests = [
        {"name": "Paris, France", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400"},
        {"name": "Dubai, UAE", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400"},
        {"name": "Bali, Indonesia", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400"},
        {"name": "Switzerland", "url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=400"}
    ]
    cols1 = st.columns(4)
    for i, d in enumerate(intl_dests):
        with cols1[i]:
            st.markdown(f'<div class="img-card"><img src="{d["url"]}" class="dest-img"><div class="dest-label">{d["name"]}</div></div>', unsafe_allow_html=True)

    # ROW 2: LOCAL
    st.markdown("<h3 style='color: white; margin-top: 20px;'>🏞️ Local Treasures</h3>", unsafe_allow_html=True)
    local_dests = [
        {"name": "Kerala Backwaters", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400"},
        {"name": "Varanasi Ghats", "url": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=400"},
        {"name": "Andaman Islands", "url": "https://images.unsplash.com/photo-1589330273594-fade1ee91647?w=400"},
        {"name": "Goa Beaches", "url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400"}
    ]
    cols2 = st.columns(4)
    for i, d in enumerate(local_dests):
        with cols2[i]:
            st.markdown(f'<div class="img-card"><img src="{d["url"]}" class="dest-img"><div class="dest-label">{d["name"]}</div></div>', unsafe_allow_html=True)

# --- 6. FOOTER ---
st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 50px; border-radius: 30px; margin-top: 80px; border-top: 1px solid #FF9933;">
        <p style='text-align: center; color: white;'>© 2026 YatriMate AI | Multi-Agent Travel Intelligence</p>
        <p style='text-align: center; color: gray;'>Saidabad, Hyderabad | +91-6304001323</p>
    </div>
""", unsafe_allow_html=True)

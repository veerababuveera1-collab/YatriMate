import streamlit as st
import google.generativeai as genai
import base64

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Festive Travel Planner",
    page_icon="🎈",
    layout="wide"
)

# --- 2. THE ULTIMATE VISUAL & AUDIO EXPERIENCE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;900&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), 
                    url("https://images.unsplash.com/photo-1530789253388-582c481c54b0?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }

    /* Balloons Animation Layer */
    .balloon-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 9999;
    }

    .hero-title {
        font-family: 'Syncopate', sans-serif;
        color: #FFFFFF;
        text-align: center;
        font-size: 4rem;
        text-shadow: 0 0 20px rgba(255,153,51,0.5);
    }

    /* Glassmorphism Cards */
    .dest-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        padding: 10px;
        transition: 0.3s;
    }
    .dest-card:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BACKGROUND MUSIC (Auto-play enabled) ---
# Note: Most browsers block autoplay until the user interacts with the page.
music_html = """
    <audio autoplay loop id="bg-music">
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
    </audio>
    <script>
        var audio = document.getElementById("bg-music");
        audio.volume = 0.2; // Setting volume to low (20%)
    </script>
"""
st.markdown(music_html, unsafe_allow_html=True)

# --- 4. BALLOONS TRIGGER ---
# Streamlit has a built-in balloon command!
if st.button("🎈 Celebrate Your Journey! 🎈"):
    st.balloons()

# --- 5. AI ENGINE ---
def generate_travel_plan(query):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "API Key missing."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.generate_content(f"Plan a trip for {query} in Telugu and English.").text

# --- 6. MAIN UI ---
st.markdown('<h1 class="hero-title">YATRIMATE AI</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center; color:#FF9933;'>Enjoy the music and plan your dream trip!</p>", unsafe_allow_html=True)

user_query = st.text_input("", placeholder="మీ ప్రయాణ గమ్యాన్ని టైప్ చేయండి...")

if st.button("Generate Plan 🚀"):
    with st.spinner("Creating Magic..."):
        result = generate_travel_plan(user_query)
        st.balloons() # Automatically fire balloons when plan is ready
        st.markdown(f'<div style="background:white; color:black; padding:30px; border-radius:20px;">{result}</div>', unsafe_allow_html=True)

# --- 7. DESTINATIONS ---
st.markdown("### 📍 Popular Picks")
dests = [
    {"name": "Maldives", "url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?q=80&w=400"},
    {"name": "Switzerland", "url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=400"},
    {"name": "Paris", "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=400"},
    {"name": "Manali", "url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?q=80&w=400"}
]

cols = st.columns(4)
for i, d in enumerate(dests):
    with cols[i]:
        st.markdown(f"""
            <div class="dest-card">
                <img src="{d['url']}" style="width:100%; border-radius:15px;">
                <p style="text-align:center; color:white; font-weight:bold; margin-top:10px;">{d['name']}</p>
            </div>
        """, unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("<br><hr><center>© 2026 YatriMate AI | Mobile: +91-6304001323</center>", unsafe_allow_html=True)

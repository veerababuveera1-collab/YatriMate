import streamlit as st
import google.generativeai as genai

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate AI - Professional Travel Engine",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SENIOR-GRADE GUI STYLING ---
st.markdown("""
    <style>
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                    url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    .hero-title {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #FF9933 !important;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    /* Image Gallery Styling - Fix for Broken Images */
    .img-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s ease;
        text-align: center;
    }
    .img-card:hover {
        transform: translateY(-5px);
        border-color: #FF9933;
    }
    .dest-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    .dest-label {
        padding: 10px;
        color: white;
        font-weight: bold;
        background: rgba(0,0,0,0.6);
    }

    div.stButton > button {
        background: linear-gradient(90deg, #FF9933, #FF5500) !important;
        color: white !important;
        width: 100%;
        border-radius: 10px !important;
        height: 50px;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE AI ENGINE ---
def generate_travel_plan(query, lang):
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key: return "Error: API Key missing."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Travel itinerary for {query} in {lang}. Include tables.")
    return response.text

if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">🚩 YatriMate AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">మీ పర్సనల్ ట్రావెల్ ఏజెంట్ | Affordable Journeys</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_query = st.text_input("", placeholder="ఎక్కడికి వెళ్లాలనుకుంటున్నారు? (ఉదా: 3 days Vizag trip...)")
    generate = st.button("Generate My Itinerary 🚀")

# --- 5. POPULAR DESTINATIONS (FIXED IMAGES) ---
if not st.session_state.itinerary_data:
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 30px;'>📍 Popular Destinations</h2>", unsafe_allow_html=True)
    
    # 1st Row: International
    col1, col2, col3, col4 = st.columns(4)
    row1 = [
        {"name": "Kerala", "url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=400&h=250&fit=crop"},
        {"name": "Dubai", "url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=250&fit=crop"},
        {"name": "Bali", "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=250&fit=crop"},
        {"name": "Singapore", "url": "https://images.unsplash.com/photo-1525625232717-1292b236f561?w=400&h=250&fit=crop"}
    ]
    
    # 2nd Row: Andhra Pradesh Focus (High Accuracy Images)
    st.markdown("<p style='text-align: center; color: #FF9933; font-weight: bold; margin-top: 20px;'>EXPLORE ANDHRA PRADESH</p>", unsafe_allow_html=True)
    col5, col6, col7, col8 = st.columns(4)
    row2 = [
        {"name": "Visakhapatnam", "url": "https://images.pexels.com/photos/14359105/pexels-photo-14359105.jpeg?auto=compress&cs=tinysrgb&w=400&h=250&fit=crop"},
        {"name": "Araku Valley", "url": "https://images.pexels.com/photos/13691355/pexels-photo-13691355.jpeg?auto=compress&cs=tinysrgb&w=400&h=250&fit=crop"},
        {"name": "Tirumala", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tirumala_090615.jpg/400px-Tirumala_090615.jpg"},
        {"name": "Gandikota", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Gandikota_Canyon_and_Pennar_River.jpg/400px-Gandikota_Canyon_and_Pennar_River.jpg"}
    ]

    all_cols = [col1, col2, col3, col4, col5, col6, col7, col8]
    all_dests = row1 + row2

    for i, dest in enumerate(all_dests):
        with all_cols[i]:
            st.markdown(f"""
                <div class="img-card">
                    <img src="{dest['url']}" class="dest-img" onerror="this.src='https://via.placeholder.com/400x250?text={dest['name']}'">
                    <div class="dest-label">{dest['name']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. RESULTS & FOOTER ---
if generate and user_query:
    with st.status("🛠️ Planning..."):
        st.session_state.itinerary_data = generate_travel_plan(user_query, "Telugu & English Mix")
        st.rerun()

if st.session_state.itinerary_data:
    st.markdown(f'<div style="background:white; color:black; padding:30px; border-radius:15px; border-left:10px solid #FF9933;">{st.session_state.itinerary_data}</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; margin-top: 50px; border-top: 1px solid #FF9933;">
        <div style="display: flex; justify-content: space-between;">
            <div>
                <h3 style="color:#FF9933;">🚩 Yatri Mate</h3>
                <p>Address: Teen Manzil Colony, Saidabad Main road, Hyderabad, Telangana 500059</p>
                <p>Mobile: +91-6304001323 | Email: veerababu.veera1@gmail.com</p>
            </div>
            <div style="text-align: right;">
                <p>• [Home](https://yatrimate.streamlit.app/)</p>
                <p>• About Us</p>
                <p>• Contact Us</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

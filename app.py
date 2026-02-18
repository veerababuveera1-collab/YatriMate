import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YatriMate | Smart Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# --- 2. DATA SOURCE ---
# Using high-quality professional image URLs from Unsplash
destinations = {
    "Singapore": {
        "image": "https://images.unsplash.com/photo-1525625239513-445c4150226c?q=80&w=1000&auto=format&fit=crop",
        "desc": "A futuristic city-state blending skyscrapers with lush botanical gardens.",
        "category": "International",
        "rating": "⭐⭐⭐⭐⭐"
    },
    "Visakhapatnam": {
        "image": "https://images.unsplash.com/photo-1590483756854-419b48f6c374?q=80&w=1000&auto=format&fit=crop",
        "desc": "The City of Destiny! Famous for its serene beaches and the INS Kursura Submarine Museum.",
        "category": "Coastal",
        "rating": "⭐⭐⭐⭐"
    },
    "Araku Valley": {
        "image": "https://images.unsplash.com/photo-1628150490184-75494d4009a2?q=80&w=1000&auto=format&fit=crop",
        "desc": "A hidden gem in the Eastern Ghats known for coffee plantations and tribal history.",
        "category": "Hill Station",
        "rating": "⭐⭐⭐⭐"
    },
    "Hyderabad": {
        "image": "https://images.unsplash.com/photo-1599395166258-202e81134268?q=80&w=1000&auto=format&fit=crop",
        "desc": "The City of Pearls, where the historic Charminar meets the modern HITEC City.",
        "category": "Heritage",
        "rating": "⭐⭐⭐⭐⭐"
    }
}

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧳 YatriMate")
    st.info("Your AI-powered travel companion.")
    
    # Search/Filter functionality
    search_query = st.text_input("Search a destination...", "").lower()
    
    st.divider()
    st.write("Built with ❤️ by [Your Name]")

# --- 4. MAIN INTERFACE ---
st.title("🌏 Explore the World")
st.markdown("Discover curated itineraries and breathtaking views.")

# Filter data based on search
filtered_destinations = {
    name: info for name, info in destinations.items() 
    if search_query in name.lower() or search_query in info['category'].lower()
}

if not filtered_destinations:
    st.warning("No destinations found matching your search.")
else:
    # Display in a grid (3 columns)
    cols = st.columns(3)
    
    for i, (city, info) in enumerate(filtered_destinations.items()):
        # Use modulo to cycle through columns
        col_index = i % 3
        
        with cols[col_index]:
            # Professional Card Container
            with st.container(border=True):
                st.image(info["image"], use_container_width=True)
                st.subheader(city)
                st.caption(f"📌 {info['category']} | {info['rating']}")
                st.write(info["desc"])
                
                if st.button(f"View Itinerary", key=city, use_container_width=True):
                    st.toast(f"Fetching details for {city}...")
                    st.write(f"### Proposed 3-Day Plan for {city}")
                    st.write("1. Arrival & Local Sightseeing\n2. Adventure & Food Tour\n3. Relaxation & Shopping")

# --- 5. FOOTER ---
st.divider()
st.caption("© 2026 YatriMate. All images sourced from Unsplash (Free License).")

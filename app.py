# --- 5. MAIN UI LAYOUT (Instructions & Settings Only) ---
# కేవలం రెండు కార్డ్‌లు మాత్రమే ఉండేలా సర్దుబాటు చేశాను
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div class="glass-card">
        <h3 style='margin-top:0; text-align: center;'>📖 Instructions</h3>
        <p>1. Enter your destination details in the box below.</p>
        <p>2. Select your preferred language for the guide.</p>
        <p>3. Click 'Generate' and let our AI build your trip!</p>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; text-align: center;'>🌐 Settings</h3>", unsafe_allow_html=True)
    
    # భాష ఎంపిక మరియు రీసెట్ బటన్ పక్కపక్కనే ఉండేలా చిన్న కాలమ్స్
    lang_col, reset_col = st.columns([2, 1])
    with lang_col:
        selected_lang = st.selectbox("Language:", ["Telugu & English Mix", "Pure Telugu", "English", "Hindi"], label_visibility="collapsed")
    with reset_col:
        if st.button("Reset App"):
            st.session_state.itinerary = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

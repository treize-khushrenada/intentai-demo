import streamlit as st

def load_sidebar_layout():
    
    return st.sidebar.markdown("""
            <style>
            [data-testid='stSidebarNav'] > ul {
                min-height: 80vh;
                min-width: 10vh;
            } 
            </style>
            """, unsafe_allow_html=True)

def sidebar_components():

    components =(

    st.selectbox(label="bot dropdown", label_visibility="hidden", options=(30, 2023120501, 2023120502, 2023120503, 2023120504, 2023120505, 2023120506, 2023120507, 1127), index=None, placeholder="Select chatbot id", key='bot_id'),
    st.text_input('Authentication Key', placeholder = 'eyJhbGci...', key="auth_token"),
    st.sidebar.write("""Gen AI Bot Builder"""), 
    st.link_button("Refine Bot", "https://intentai.org/"),
    st.sidebar.write("""Copyright © 2024 Intent AI All rights reserved.""")

    )

    return components
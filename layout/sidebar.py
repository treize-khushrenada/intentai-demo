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

    return st.sidebar.write("""Gen AI Bot Builder"""), st.link_button("Refine Bot", "https://ematest.streamlit.app/"),st.sidebar.write("""Copyright © 2023 Intent AI All rights reserved.""")


    
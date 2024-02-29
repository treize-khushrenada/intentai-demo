import streamlit as st
import random

def load_configure_page_layout():
    
    return st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            border:0px ;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            border:0px ;
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
)

def load_tab_layout():
    
    return st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.2rem;
    }
    </style>
    """,unsafe_allow_html=True
)


def add_text_input_row(input_name, default_text=''):
    return st.text_input(f'{input_name} {st.session_state.count}', value=default_text)
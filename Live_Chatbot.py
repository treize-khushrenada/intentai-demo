import streamlit as st
from layout.sidebar import load_sidebar_layout, sidebar_components

import sys
sys.path.append("..")
import time
import requests
import json
import os
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
auth_token = st.secrets["AUTH_TOKEN"]
headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {auth_token}'
            }

from langchain.schema import ChatMessage
from langchain.callbacks import StreamlitCallbackHandler

if 'bot_id' not in st.session_state:
    st.session_state['bot_id'] = 30
if 'auth_token' not in st.session_state:
    st.session_state['auth_token'] = "eyJhbGciOiJIUzI1NiIsImtpZCI6InZwTG9yTHk3anZLVktEVjAiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzA5MjA1NzMwLCJpYXQiOjE3MDkxMTkzMzAsImlzcyI6Imh0dHBzOi8vem51dnR1d3Zocmp2c2t4anJ2a2Yuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjMwM2JjYjY4LTEzNGMtNDBiOS04NzYzLWJlZjU0OWNhZWFkMyIsImVtYWlsIjoiYXJ0aHVyKzNAaW50bnQuYWkiLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7fSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTcwOTExOTMzMH1dLCJzZXNzaW9uX2lkIjoiYTEyMDJlZGQtMTFkYS00MmZkLWI2N2MtZWU0ZWI2NjZjYzQwIn0.GJzakmFGavuRI32uf5srYH2Hmn35vj_bk20kFI1PcZE"

# page information
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

# load sidebar
with st.sidebar:
    load_sidebar_layout()
    sidebar_components()


st.title(
    """Live Gen AI  """
)

if 'rag_hierarchy' not in st.session_state:
    st.session_state['rag_hierarchy'] = 0

def render_chat_interface():
    #chat interface
    if "messages" not in st.session_state:
        st.session_state["messages"] = [ChatMessage(role="assistant", content="Hi! Type your query here and I will try my best to provide an answer.")]

    for msg in st.session_state.messages:
        st.chat_message(msg.role).write(msg.content)

def get_response(prompt, callback_handler):
    response = st.session_state['chatbot'].handle_message(prompt, callback_handler)
    return response

if __name__ == '__main__':
    # get layout of chat interface
    st.write("Hello World")
    render_chat_interface()
    
    # handle user input
    prompt = st.chat_input()
    if prompt:
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        st.chat_message("user").write(prompt)
        
    # call ai messag
        with st.chat_message("assistant"):
            
            # st_callback = StreamlitCallbackHandler(st.container())
            # response = get_response(prompt, st_callback)
            with st.spinner("Thinking..."):
                bot_id_str = str(st.session_state['bot_id'])
                converse_url = f"https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/converse/text/botid={bot_id_str}"
                
                
                covnerse_response = requests.post(converse_url, json={"user_id": 1, "bot_id": st.session_state['bot_id'], "user_utterance": prompt}, headers=headers).json()
            
            st.session_state.messages.append(ChatMessage(role="assistant", content=covnerse_response['bot_message']))
            
            st.rerun()

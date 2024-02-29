import streamlit as st
from layout.sidebar import load_sidebar_layout, sidebar_components

import sys
sys.path.append("..")
import time
import requests
import os
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

from langchain.schema import ChatMessage
from langchain.callbacks import StreamlitCallbackHandler

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
                covnerse_response = requests.post("https://9405-223-19-159-62.ngrok.app/converse/text/botid=1127", json={"user_id": 1, "bot_id": 1127, "user_utterance": prompt}).json()
            
            st.session_state.messages.append(ChatMessage(role="assistant", content=covnerse_response['bot_message']))
            
            st.rerun()

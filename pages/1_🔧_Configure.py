# streamlit frontend
import streamlit as st
from layout.sidebar import load_sidebar_layout, sidebar_components
from layout.page import load_configure_page_layout, load_tab_layout

# backend api calls
import requests
import time
# text processing from files
from io import StringIO

import sys
sys.path.append("..")

from connections.supabase import get_supabase_client, upload_file

pre_msg_number = 0

# initialize the session states on different tabs
# cross tabs
if 'bot_id' not in st.session_state:
    st.session_state['bot_id'] = 1127

if 'bot_info' not in st.session_state:
    st.session_state['bot_info'] = {
                                    "user_id" : 1, 
                                    "bot_id" : st.session_state['bot_id'], 
                                    "custom_knowledge" : None,
                                    "custom_persona" : None,
                                    "llm_name" : None,
                                    "embedding_name" : None
                                    }

# under knowledge tab
if 'kb_toggle' not in st.session_state:
    st.session_state['kb_toggle'] = True
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0
if 'knowledge_cluster_created' not in st.session_state:
    st.session_state['knowledge_cluster_created_button'] = False
if 'upload_complete' not in st.session_state:
    st.session_state['upload_complete'] = None

# under persona & behavior tab
if 'thought_process' not in st.session_state:
    st.session_state['thought_process'] = False  
if 'role' not in st.session_state:
    st.session_state['role'] = "General Chatbot"  
if 'personality' not in st.session_state:
    st.session_state['personality'] = "Friendly"  
if 'format_instructions' not in st.session_state:
    st.session_state['format_instructions'] = ""
if 'extra_prompt' not in st.session_state:
    st.session_state['extra_prompt'] = ""  
if 'num_tasks' not in st.session_state:
    st.session_state['num_tasks'] = 1
if "other_tasks" not in st.session_state:
    st.session_state["other_tasks"] = []
if "task_primary" not in st.session_state:
    st.session_state["task_primary"] = [""]
if "tasks" not in st.session_state:
    st.session_state['tasks'] = ""
if "new_task" not in st.session_state:
    st.session_state["new_task"] = ""
if 'tasks_list' not in st.session_state:
    st.session_state['tasks_list'] = []


# under advanced tab
if 'chosen_llm' not in st.session_state:
    st.session_state.chosen_llm = 'gpt-35-turbo-16k'
if 'chosen_embedding' not in st.session_state:
    st.session_state.chosen_embedding = 'openai_embedding'
if 'chain_type' not in st.session_state:
    st.session_state['chain_type'] = 'stuff'
if 'k' not in st.session_state:
    st.session_state['k'] = 10
if 'rag_hierarchy' not in st.session_state:
    st.session_state['rag_hierarchy'] = 0

# define frontend actions
def add_text_input_row(input_name, default_text=''):
    return st.text_input(f'{input_name} {st.session_state.count}', value=default_text)

def file_uploader_status():
    st.session_state['upload_complete'] = False

def remove_knowledge_cluster():
    del st.session_state['memory_collection']
    del st.session_state['qa_chain_collection']

    st.session_state['knowledge_cluster_created_button'] = False


    #st.write({"force_reference": force_reference, "remember_conversation": remember_conversation, "pre_msg_number": pre_msg_number})

# if 'chatbot' not in st.session_state:
#     update_chatbot()

# # page information
# st.set_page_config(
#     page_title="Home",
#     page_icon="🏠",
# )

# load sidebar
with st.sidebar:
    load_sidebar_layout()
    sidebar_components()

with st.container():
    col1, col2 = st.columns(2)
    load_configure_page_layout()
    with col1:
        st.markdown(
            """### 🔧 Configure"""
        )


# tabs for configurations
tab_knowledge, tab_persona_behavior, tab_channels, tab_advanced = st.tabs(["📚 Knowledge", "👤 Persona & Skills", "💬 Channels", "🧠 Advanced"])
load_tab_layout()

with tab_knowledge:
    on = st.toggle('Use Custom Knowledge Base', key='kb_toggle', value=False)
    
    if on:
        
        st.session_state['bot_info']['custom_knowledge'] = True
        
        botinfo_response = requests.post('https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/bot-info/update', headers={"Content-Type": "application/json"}, json = st.session_state['bot_info'])
        print(botinfo_response)         
        if botinfo_response.json()['status'] == 'success':

            st.success('Custom Knowledge Base: On')

        else:
            
            st.error("Error: Could not update knowledge base, please contact support for assistance.")

        with st.container():
            
            st.write("**1. Define Cluster**")

            st.session_state['cluster_desc'] = st.text_input('Describe the Cluster', placeholder = 'to help chatbot understand it better')
            st.session_state['related_tasks'] = st.text_area('Related Tasks', value = st.session_state.get('related_tasks', ''), placeholder = 'to help chatbot understand it better (i.e. Useful for when...)')
            st.session_state['usage_instructions'] = st.text_area('Usage Instructions', value = st.session_state.get('usage_instructions', ''), placeholder = 'to help chatbot understand it better (i.e. Tasked to...)')

            # knowledge_clusters_removed = st.button('Clear All Clusters', key="knowledge_clusters_removed", on_click=remove_knowledge_cluster)

        # Display the default values for doc_desc and doc_instruct based on the settings in config_manager
        # create_qa_config()
        with st.container():

            st.write("**2. Upload Documents**")
            st.session_state['list_documents'] = st.file_uploader("Support .txt, .md, .html files", accept_multiple_files=True, key=st.session_state["file_uploader_key"], on_change=file_uploader_status)
            
        with st.container():
            #st.write("Choose")
            for i, uploaded_file in enumerate(st.session_state['list_documents']):
                document_selected = st.checkbox(uploaded_file.name, value=True)
                
                if document_selected:
                    document_desc = st.text_input('Describe the document', placeholder = 'to help chatbot understand it better', key=uploaded_file.name+'input')
                    st.session_state['list_documents'][i] = {"filename": uploaded_file.name, "included" : True, "description" : document_desc, "file_object" : uploaded_file}
                else:
                    st.session_state['list_documents'][i]= {"filename":uploaded_file.name, "included" : False}
            
        with st.container():
            
            knowledge_cluster_created = st.button('Update Knowledge', key="knowledge_cluster_created")

            if knowledge_cluster_created:

                st.session_state['included_documents'] = [document for document in st.session_state['list_documents'] if document['included']]
                # stringio_documents = [StringIO(text_file['file_info'].getvalue().decode("utf-8")) for text_file in st.session_state['included_documents']]
                # text_documents = [io_document.read() for io_document in stringio_documents]
                text_documents_info = [{"filename": document['filename'], "description": document['description']} for document in st.session_state['included_documents']]

                memory_config = {
                                'user_id' : 1,
                                'bot_id' : st.session_state['bot_id'],
                                'cluster_desc' : st.session_state['cluster_desc'],
                                'related_tasks' : st.session_state['related_tasks'],
                                'usage_instructions': st.session_state['usage_instructions'],
                                'text_documents_info' : text_documents_info
                                }

                if st.session_state['upload_complete'] == False:
                    with st.spinner('uploading file...'):
                        for document in st.session_state['list_documents']:
                            upload_file(document)
                        st.session_state['upload_complete'] = True
            
                with st.spinner('updating vector store...'):
                    try:
                        
                        kb_update_response = requests.post('https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/memory/update', headers={"Content-Type": "application/json"}, json = memory_config)
                        
                        if kb_update_response.json()['status'] == 'success':

                            st.success('Knowledge base updated successfully.')

                        else:
                            st.error("Error: Could not update knowledge base, please contact support for assistance.")
                    
                    except:
                        st.error("Error: Could not connect to the knowledge base server, please contact support for assistance.")
                        
                    
                # create new vector store collection and update it with the new memory unit
                # st.session_state['memory_update_status'] = requests.post('http://localhost:8000/memory-update', data = memory_config)
                
                # reset the text fields after memory unit is created
                st.session_state['cluster_desc'] = ""
                st.session_state['related_tasks'] = ""
                st.session_state['usage_instructions'] = ""
                st.session_state['list_documents'] = []
                st.session_state['knowledge_cluster_created_button'] = True
                st.session_state["file_uploader_key"] += 1
                
                # st.write(memory_config)
                            
        with st.expander("Database Connection (developers only)", expanded=False):    
            st.write("Connect Database Table (PostgreSQL)")
            db_desc = st.text_input('Related Tasks', placeholder = 'to help chatbot understand it better (i.e. Useful for when...)', key='db_desc')
            db_instruct = st.text_input('Usage Instructions', placeholder = 'to help chatbot understand it better (i.e. Tasked to...)', key='db_instruct')
            db_host = st.text_input('Host', placeholder = '', key='db_host')
            db_user = st.text_input('User', placeholder = '', key='db_user')
            db_password = st.text_input('Password', placeholder = '', key='db_password')
            db_port = st.text_input('Port', placeholder = '', key='db_port')
            db_name = st.text_input('Name', placeholder = '', key='db_name')
            db_sql_query = st.text_input('SQL Query', placeholder = '', key='db_sql_query')
            db_tool_save = st.button('Save', key='db_save')
            
            if db_tool_save:
                db_tool_prefs = [db_desc, db_instruct, db_host, db_user, db_password, db_port, db_name, db_sql_query]
                st.write(db_tool_prefs)
            
            st.write("Connect Vector Store (via Supabase)")
            vector_store_desc = st.text_input('Related Tasks', placeholder = 'to help chatbot understand it better (i.e. Useful for when...)', key='vector_store_desc')
            vector_store_instruct = st.text_input('Usage Instructions', placeholder = 'to help chatbot understand it better (i.e. Tasked to...)', key='vector_store_instruct')
            vs_host = st.text_input('Host', placeholder = '', key='vs_host')
            vs_user = st.text_input('User', placeholder = '', key='vs_user')
            vs_password = st.text_input('Password', placeholder = '', key='vs_password')
            vs_port = st.text_input('Port', placeholder = '', key='vs_port')
            vs_db_name = st.text_input('DB Name', placeholder = '', key='vs_db_name')
            vs_collection_name = st.text_input('Collection Name', placeholder = '', key='vs_collection_name')
            vs_tool_save = st.button('Save', key='vs_save')
            
            if vs_tool_save:
                vs_tool_prefs = [vector_store_desc, vector_store_instruct, vs_host, vs_user, vs_password, vs_port, vs_db_name, vs_collection_name]
                st.write(vs_tool_prefs)
    
    else:
        st.session_state['rag_hierarchy'] = 0
        
        st.session_state['bot_info']['custom_knowledge'] = False
        
        botinfo_response = requests.post('https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/bot-info/update', headers={"Content-Type": "application/json"}, json = st.session_state['bot_info'])
                        
        if botinfo_response.json()['status'] == 'success':

            st.success('Custom Knowledge Base: Off')
            st.write("Chatbot will use the default knowledge of the AI Model")

        else:
            
            st.error("Error: Could not update knowledge base, please contact support for assistance.")


with tab_persona_behavior:
    
    thought_process = st.toggle('Customized Persona & Skills', key='agent_hierarchy', value=True)
    
    if thought_process:
        
        st.session_state['bot_info']['custom_persona'] = True
        
        botinfo_response = requests.post('https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/bot-info/update', headers={"Content-Type": "application/json"}, json = st.session_state['bot_info'])
                        
        if botinfo_response.json()['status'] == 'success':

            st.success('Custom Persona & Skills: On')

        else:
            
            st.error("Error: Could not update persona & skills, please contact support for assistance.")

        # create_agent_config()
        def persona_manager():
            with st.container():
                st.write("**Persona**")
                chatbot_role_prompt = st.text_input('Role', placeholder = 'what is the role the chatbot? such as position in a company', key='role')
                chatbot_personality_prompt = st.text_input('Personality', placeholder = 'what is the tone of voice/ manner?', key='personality')

        def skills_manager():
            with st.container():
                st.write("**Skills**")
                user_input = st.text_input(f'Describe and click "Add":', value='General chit-chat', placeholder = 'what is the chatbot expected to do?')
                add_button = st.button("Add", key='add_task_button')
                if add_button:
                    if len(user_input) > 0:
                        st.session_state['tasks_list'] += [user_input]
                        # st.write( st.session_state['tasks_list'] )
                        for idx, task in enumerate(st.session_state['tasks_list']):
                            st.write(f'Task {idx+1}: {task}')
                    else:
                        st.warning("Enter text")
                remove_task_button = st.button("Reset Skills", key=f'remove_tasks_button')
                if remove_task_button:
                    st.session_state['tasks_list'] = []
                    # st.write(st.session_state['tasks_list'] )

        def persona_skills_prefs_record():
            with st.expander("Prompts Preview (developer)", expanded=False):

                tasks_string = " /n ".join([f"{i+1}. {task}" for i, task in enumerate(st.session_state['tasks_list'])])

                st.session_state['tasks'] = f"""
                    Your professional service scope is only about: 
                    {tasks_string}
                    If you cannot identify the service type, or the user's query is out of your professional service scope, politely end the conversation. 
                    """

                st.write({"role_prompt": st.session_state['role'], "personality_prompt": st.session_state['personality'], "tasks_prompt" : st.session_state['tasks']})

        persona_manager()
        
        skills_manager()

        persona_skills_prefs_record()

        with st.container():

            persona_skills_updated = st.button('Update Persona & Skills', key="persona_skills_updated")

            if persona_skills_updated:
                
                with st.spinner('updating persona & skills...'):
                    
                    try:
                            perona_skills_config = {
                                                "user_id" : 1,
                                                "bot_id" : st.session_state['bot_id'],
                                                "role_prompt": st.session_state['role'], 
                                                "personality_prompt": st.session_state['personality'], 
                                                "tasks_prompt" : st.session_state['tasks']
                                                }

                            persona_skills_update_response = requests.post('https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/persona-skills/update', headers={"Content-Type": "application/json"}, json = perona_skills_config)
                            

                            if persona_skills_update_response.json()['status'] == 'success':

                                st.success('Persona and skills updated successfully.')

                            else:
                                
                                st.error("Error: Could not update persona and skills, please contact support for assistance.")
                    
                    except:
                            
                            st.error("Error: Could not connect to the server, please contact support for assistance.")
                #update_chatbot(st.session_state['chosen_llm'], st.session_state['chosen_embedding'], st.session_state['rag_hierarchy'], st.session_state['role'], st.session_state['personality'], st.session_state['tasks'], st.session_state['format_instructions'], st.session_state['agent_extra_prompt'])
            
            st.button("Reset All Settings")
        
    else:

        st.session_state['bot_info']['custom_persona'] = False
            
        botinfo_response = requests.post('https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/bot-info/update', headers={"Content-Type": "application/json"}, json = st.session_state['bot_info'])
                            
        if botinfo_response.json()['status'] == 'success':

            st.success('Custom Persona & Skills: On')

        else:
                
            st.error("Error: Could not update persona & skills, please contact support for assistance.")
                
with tab_advanced:
    st.write("### Advanced Chatbot Settings")
    
    # Allow users to choose the LLM (Language Model)
    llm_options = ['gpt-35-turbo-16k', 'gpt-35-turbo', 'bedrock_claude_2']
    st.session_state['chosen_llm'] = st.selectbox('Choose a Language Model:', options=llm_options, index=llm_options.index(st.session_state['chosen_llm']))
    # st.write(f"Chosen Language Model: {st.session_state['chosen_llm']}")

    # Allow users to choose the embedding option
    embedding_options = ['openai_embedding', 'titan_embedding']
    st.session_state['chosen_embedding'] = st.selectbox('Choose an Embedding Option:', options=embedding_options, index=embedding_options.index(st.session_state['chosen_embedding']))
    # st.write(f"Chosen Embedding: {st.session_state['chosen_embedding']}")

    with st.container():

        advanced_settings_updated = st.button('Update Advanced Settings', key="advanced_settings_updated")

        if advanced_settings_updated:
            
            with st.spinner('Updating advanced settings...'):
                    
                try:
                        
                        st.session_state['bot_info']['llm_name'] = st.session_state['chosen_llm']
                        st.session_state['bot_info']['embedding_name'] = st.session_state['chosen_embedding']
                        
                        botinfo_update_response = requests.post('https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/bot-info/update', headers={"Content-Type": "application/json"}, json = st.session_state['bot_info'])
                            
                        if botinfo_update_response.json()['status'] == 'success':

                            st.success('Advanced settings updated successfully.')

                        else:
                                
                            st.error("Error: Could not update advanced settings, please contact support for assistance.")
                    
                except:
                    
                    st.error("Error: Could not connect to the server, please contact support for assistance.")
with tab_channels:    
    st.write("**Instant Messenger (WhatsApp/ Telegram/ WeChat/ Facebook Messenger/ Line)**")
    st.write("Paste this link to your BSP account:")
    bot_id_str = str(st.session_state['bot_id'])
    txt = st.code(f"https://ema-intnt-app340275ed.whitehill-762226dd.centralindia.azurecontainerapps.io/converse/text/botid={bot_id_str}", language="markdown")
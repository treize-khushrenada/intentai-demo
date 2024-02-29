from st_supabase_connection import SupabaseConnection
import streamlit as st

def get_supabase_client():

    supabase_client = st.connection(
    name="genai-bot-builder",
    type=SupabaseConnection,
    ttl=None,
    url="https://lxfznzescvbrerjcgdil.supabase.co", # not needed if provided as a streamlit secret
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx4ZnpuemVzY3ZicmVyamNnZGlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDAwMTM1NTMsImV4cCI6MjAxNTU4OTU1M30.Xq6y4VIcdo1EP37gG4gTt9s70sxF1zxOdXUA6URphnM"
    )

    return supabase_client

def upload_file(file):

    supabase_client = get_supabase_client()
    file_name = file['filename'] 
    file_object = file['file_object']
    
    supabase_client.upload("kb_files_1127", source='local', file=file_object, destination_path=file_name, overwrite='true')
    st.toast(f'file {file_name} uploaded')
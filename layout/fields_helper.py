import streamlit as st

def add_field():
    st.session_state.fields_size += 1

def delete_field(index):
    st.session_state.fields_size -= 1
    del st.session_state.fields[index]
    del st.session_state.deletes[index]

if "fields_size" not in st.session_state:
    st.session_state.fields_size = 0
    st.session_state.fields = []
    st.session_state.deletes = []

# fields and types of the table
for i in range(st.session_state.fields_size):
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.fields.append(st.text_input(f"Field {i}", key=f"text{i}"))

    with c2:
        st.session_state.deletes.append(st.button("❌", key=f"delete{i}", on_click=delete_field, args=(i,)))

st.button("➕ Add field", on_click=add_field)
if st.button("Submit"):
    st.write(st.session_state.text0)
    st.write(st.session_state.text1)
    st.write(st.session_state.text2)
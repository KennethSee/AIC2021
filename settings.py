import streamlit as st


def check_session():
    if 'session_id' not in st.session_state:
        return False
    else:
        return True


def set_session(session_id):
    st.session_state['session_id'] = session_id


def clear_session():
    for key, value in st.session_state.items():
        st.session_state.pop(key, None)

def get_session_id():
    return st.session_state['session_id']

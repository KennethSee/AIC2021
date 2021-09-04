import pandas as pd
import streamlit as st

from settings import check_session


def app():
    if check_session():
        if 'fs_raw' in st.session_state:
            st.dataframe(st.session_state['fs_raw'])
        else:
            st.info('You have not uploaded any financial information yet.')
    else:
        st.info('Please log in first.')
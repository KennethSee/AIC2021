import pandas as pd
import streamlit as st

from utils.settings import check_session, get_session_id
from utils.financials import retrieve_financials


def app():
    if check_session():
        db = st.session_state['db']
        df = retrieve_financials(db)
        if df is not None:
            st.session_state['fs'] = df
            st.dataframe(df)
        else:
            st.info('You have not uploaded any financial information yet.')
    else:
        st.info('Please log in first.')

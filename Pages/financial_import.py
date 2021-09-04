import pandas as pd
import streamlit as st

from settings import check_session


def app():
    if check_session():
        uploaded_file = st.file_uploader('Upload your P&L template')
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if format_check(df):
                    st.dataframe(df)
                else:
                    st.error('Unable to read uploaded file. Please make sure the format of the file matches the template.')
            except:
                st.error('Unable to read uploaded file. Please make sure the format of the file matches the template.')

            # commit financials
            if st.button('Commit Financials'):
                st.session_state['fs_raw'] = df
                st.success('Commit successful')
    else:
        st.info('Please log in first.')


def format_check(df):
    '''
    Check that format of uploaded file conforms to template standard
    '''
    if df.columns[1] != 'Direction' or df.columns[2] != 'IsFixed':
        return False

    return True

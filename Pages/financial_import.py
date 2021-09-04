import pandas as pd
import streamlit as st

from settings import check_session, get_session_id


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
                insert_financials(df)
                st.success('Commit successful')
    else:
        st.info('Please log in first.')


def format_check(df):
    '''
    Check that format of uploaded file conforms to template standard
    '''
    if df.columns[1] != 'SortOrder' or df.columns[2] != 'Direction' or df.columns[3] != 'IsFixed':
        return False

    return True


def insert_financials(df):
    company_id = get_session_id()
    db = st.session_state['db']

    items = df.iloc[:, 0].tolist()
    sort_order = df.iloc[:, 1].tolist()
    direction = df.iloc[:, 2].tolist()
    is_fixed = df.iloc[:, 3].tolist()
    mappings = {}
    for k in range(len(items)):
        mappings[items[k]] = {
            'sortOrder': sort_order[k],
            'direction': direction[k],
            'isFixed': is_fixed[k]
        }
    db.update_mappings(company_id, mappings)

    # create individual financial entries by date
    for i in range(4, df.shape[1]):
        date = df.iloc[:, i].name
        info = df.iloc[:, i].tolist()
        financial_entry = {}
        for j in range(len(items)):
            financial_entry[items[j]] = info[j]
        db.insert_financials(company_id, date, financial_entry)

import streamlit as st

from utils.settings import check_session, get_session_id


def app():
    if check_session():
        db = st.session_state['db']
        company_id = get_session_id()

        retrieved_drivers = db.get_company_drivers(company_id)

        if db.get_company_financials(company_id) is None:
            st.info('Please upload a set of financials first.')
        elif retrieved_drivers is None:
            st.info('Please create drivers in the Manage Drivers page.')
        else:
            financial_dates = db.get_financial_dates(company_id)
            st.write(financial_dates)

    else:
        st.info('Please log in first.')

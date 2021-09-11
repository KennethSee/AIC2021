import streamlit as st

from utils.settings import check_session, get_session_id
from utils.financials import retrieve_financials
from Objects.driver import Driver
from Objects.fs import FS


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
            drivers = sorted([Driver(driver, values) for driver, values in retrieved_drivers.items()],
                             key=lambda x: x.name)
            n_drivers = len(drivers)
            financials = FS(retrieve_financials(db))
            financial_items = financials.get_fs_variable_items()

            st.header('Map drivers to relevant financial statement items')

            driver_map = {}
            for item in financial_items:
                item_map = []
                cols = st.columns(n_drivers + 1)
                cols[0].write(item)
                for i in range(1, n_drivers + 1):
                    to_map = cols[i].checkbox(drivers[i-1].name, key=f'{item}_{drivers[i-1].name}_map')
                    if to_map:
                        item_map.append(drivers[i-1])
                driver_map[item] = item_map

        # save driver map to session
        st.session_state['driver_map'] = driver_map

    else:
        st.info('Please log in first.')

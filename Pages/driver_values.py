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
            st.header('Enter driver values')
            financial_dates = db.get_financial_dates(company_id)
            n_financials = len(financial_dates)

            # driver containers
            drivers = sorted([key for key, value in db.get_company_drivers(company_id).items()])
            drivers_data_dict = {driver: [None] * n_financials for driver in drivers}
            for driver in drivers:
                with st.expander(driver, expanded=True):
                    # data for drivers
                    driver_data = retrieved_drivers[driver]
                    for i in range(n_financials):
                        date = financial_dates[i]
                        cols = st.columns(2)
                        cols[0].write(date)
                        drivers_data_dict[driver][i] = cols[1].number_input(
                            label='',
                            value=float(extract_data(driver_data, date)),
                            format='%f',
                            key=f'{driver}_{date}'
                        )

            if st.button('Commit Driver Data'):
                commit_data(db, company_id, drivers_data_dict, financial_dates)
                st.success('Driver data have been updated.')

    else:
        st.info('Please log in first.')


def extract_data(data: dict, extract_key: str):
    if extract_key in data:
        x = data[extract_key]
    else:
        x = 0.0
    return x


def commit_data(db, company_id, data, dates):
    for driver, values in data.items():
        data_info = {}
        for i in range(len(dates)):
            data_info[dates[i]] = values[i]
        db.insert_driver(company_id, driver, data_info)

import pandas as pd
import streamlit as st

from utils.settings import check_session, get_session_id
from utils.financials import retrieve_financials
from Objects.driver import Driver
from Objects.fs import FS
from Models.bootstrap_lasso import BootstrapLasso


def app():
    if check_session():
        db = st.session_state['db']
        company_id = get_session_id()

        retrieved_drivers = db.get_company_drivers(company_id)

        if db.get_company_financials(company_id) is None:
            st.info('Please upload a set of financials first.')
        elif retrieved_drivers is None:
            st.info('Please create drivers in the Manage Drivers page.')
        elif 'driver_map' not in st.session_state:
            st.info('Please map drivers in the Map Drivers page.')
        else:
            drivers = sorted([Driver(driver, values) for driver, values in retrieved_drivers.items()],
                             key=lambda x: x.name)
            st.header('Execute forecast')

            st.subheader('Enter driver values for the next time period')
            next_driver_input = {}
            for driver in drivers:
                next_driver_input[driver.name] = [st.number_input(driver.name, key=f'next_value_for_{driver.name}')]

            if st.button('Look into the future!'):
                fs = FS(retrieve_financials(db))

                forecast = {}
                for item in fs.get_fs_variable_items():
                    # train Lasso model
                    train_df = fs.df_processed[['date', item]]
                    for driver in st.session_state['driver_map'][item]:
                        train_df = train_df.merge(driver.df, how='inner', left_on='date', right_on='date')
                    model = BootstrapLasso(train_df, item)
                    model.train()

                    # make prediction
                    prediction = model.predict(pd.DataFrame.from_dict(next_driver_input))

                    forecast[item] = prediction

                st.success('Forecast generated')

                for key, val in forecast.items():
                    cols = st.columns(2)
                    cols[0].write(key)
                    cols[1].write(val)

    else:
        st.info('Please log in first.')
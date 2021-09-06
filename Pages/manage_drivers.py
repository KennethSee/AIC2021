import streamlit as st

from utils.settings import check_session, get_session_id


def app():
    if check_session():
        db = st.session_state['db']
        company_id = get_session_id()

        if db.get_company_financials(company_id) is None:
            st.info('Please upload a set of financials first.')
        else:
            st.header('Create a new driver')
            driver_name = st.text_input('Driver name')
            if st.button('Add Driver'):
                if driver_name == '':
                    st.error('Please include a name for the driver you wish to add.')
                elif check_existing_driver(db, company_id, driver_name):
                    st.error('This driver has already been created!')
                else:
                    db.insert_driver(company_id, driver_name, {})
                    st.success(f'Successfully added {driver_name} as a driver!')

            # display existing drivers
            drivers = [key for key, value in db.get_company_drivers(company_id).items()]
            if len(drivers) != 0:
                st.subheader('Existing drivers')
                for driver in drivers:
                    st.write(driver)
                    if st.button('Delete', key=f'{driver}_delete'):
                        db.delete_driver(company_id, driver)
                        st.info(f'{driver} has been deleted.')

    else:
        st.info('Please log in first.')


def check_existing_driver(db, company_id, driver_id):
    if driver_id in db.get_company_drivers(company_id):
        return True
    else:
        return False

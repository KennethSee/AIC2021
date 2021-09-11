import streamlit as st

from Pages.multi_page import MultiPage
from Pages import login, financial_import, view_financials, manage_drivers, driver_values, map_drivers, prediction
from db import DB

def main():
    app = MultiPage()
    st.session_state['db'] = DB('secrets/aic2021-b72a6-firebase-adminsdk-cs1gs-777235e9ad.json')

    st.title('ACCOUNTING INNOVATION CHALLENGE 2021')

    # page applications
    app.add_page('Login', login.app)
    app.add_page('Financial Import', financial_import.app)
    app.add_page('View Financials', view_financials.app)
    app.add_page('Manage Drivers', manage_drivers.app)
    app.add_page('Set Driver Values', driver_values.app)
    app.add_page('Map Drivers', map_drivers.app)
    app.add_page('Generate Forecast', prediction.app)

    app.run()


if __name__ == '__main__':
    main()

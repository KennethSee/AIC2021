import streamlit as st
from Pages.multi_page import MultiPage
from Pages import login, financial_import, view_financials
from settings import check_session

def main():
    app = MultiPage()

    st.title('ACCOUNTING INNOVATION CHALLENGE 2021')

    # page applications
    app.add_page('Login', login.app)
    app.add_page('Financial Import', financial_import.app)
    app.add_page('View Financials', view_financials.app)

    app.run()


if __name__ == '__main__':
    main()

import streamlit as st
import time

import settings


def app():
    if settings.check_session():
        st.write(f'Hi {settings.get_session_id()}!')
        st.write('You are already logged in. Would you like to log out?')
        if st.button('Logout'):
            settings.clear_session()
            st.success('You have successfully logged out.')
    else:
        username = st.text_input('What is your company name?', key='login_username')
        login = st.button('Login')

        if login:
            if username != '':
                settings.set_session(username)
                st.success(f'Welcome {username}!')
            else:
                st.error('Please fill in all required fields')


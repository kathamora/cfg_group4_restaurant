import streamlit as st
from user_authenticator import UserAuthenticator, mydb


def show_signup():
    st.subheader("Create a new account")
    email = st.text_input("Email", key="email_input")
    username = st.text_input("Username (Username must start with an alphabet and consist of 8 characters at minimum)",
                             key="username_input2")
    password = st.text_input("Password (Password must consist of 8 characters at minimum)", type='password',
                             key="password_input2")
    signup_button = st.button("Create my account")
    if signup_button:
        try:
            authenticator = UserAuthenticator(mydb)

            # Check if email already exists
            email_exists = authenticator.check_email_exists(email)
            if email_exists:
                st.error("Email already exists")
                return None

            # Check if username already exists
            username_exists = authenticator.check_username_exists(username)
            if username_exists:
                st.error("Username already exists")
                return None

            username, password, email = authenticator.signup(email, username, password)
            st.success("Account created successfully")
            return username, password, email
        except ValueError as e:
            st.error(str(e))


def show_login():
    username = st.text_input("Username", key="username_input1")
    password = st.text_input("Password", type='password', key="password_input1")
    login_button = st.button("Log-in", key="login_button1")
    if login_button:
        try:
            authenticator = UserAuthenticator(mydb)

            # Check if username exists
            username_exists = authenticator.check_username_exists(username)
            if not username_exists:
                st.error("Username does not exist")
                return None

            user_id, retrieved_username, email, retrieved_password = authenticator.get_user_info("username", username)
            if password != retrieved_password:
                print(authenticator.get_user_info("username", username))
                st.error("Incorrect password")
                return None

            st.success("Logged in as {}".format(username))

            return username, password
        except ValueError as e:
            st.error(str(e))


def get_signup_login_choice():
    choice = st.radio("Sign up/Login", ['Sign up', 'Login'])
    return choice


def login_signup_choice(mydb, choice=None):
    username = None
    password = None
    email = None

    if st.session_state.get('user_info'):
        username, password, email = st.session_state['user_info']

    if choice == 'Sign up':
        user_info = show_signup()
        if user_info:
            username, password, email = user_info
            st.session_state['user_info'] = (username, password, email)
    elif choice == 'Login':
        user_info = show_login()
        if user_info:
            username, password = user_info
            st.session_state['user_info'] = (username, password, email)

    return username, password, email




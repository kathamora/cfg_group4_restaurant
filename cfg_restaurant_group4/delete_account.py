import streamlit as st
from sql_connection import mydb, DbConnectionError
from user_authenticator import UserAuthenticator

def delete_my_account(username):
    try:
        authenticator = UserAuthenticator(mydb)
        user_id = authenticator.get_user_info("username", username)

        ask_user = st.checkbox("Are you sure you want to delete your account?")
        if ask_user:
            cursor = mydb.cursor()
            cursor.execute("DELETE FROM users WHERE user_ID = %s", (user_id,))
            mydb.commit()
            st.success(f"Your account has been deleted.")

    except DbConnectionError as error:
        st.error("An error occurred while trying to delete your account. Please try again later.")
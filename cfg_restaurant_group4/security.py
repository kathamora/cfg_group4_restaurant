import streamlit as st
from sql_connection import mydb, DbConnectionError
from user_authenticator import UserAuthenticator

class DbConnectionError(Exception):
    pass

def login_security_page(username):
    st.header("Login and Security")
    authenticator = UserAuthenticator(mydb)
    try:
        mydb.ping(reconnect=True)  # Ping the database to ensure the connection is still available
    except mydb.OperationalError:
        st.error("Failed to connect to the database.")
        return

    user_id, retrieved_username, retrieved_email, retrieved_password = authenticator.get_user_info("username", username)

    if st.checkbox('Password change'):
        current_password = st.text_input("Confirm Password:", type="password")
        new_password = st.text_input("New Password:", type="password")
        if st.button("Update Password"):
            try:
                cursor = mydb.cursor()
                cursor.execute(f"SELECT password FROM users WHERE username = '{retrieved_username}'")
                result = cursor.fetchone()
                db_password = result[0]
                if db_password != current_password:
                    st.error("Current password is incorrect!")
                else:
                    cursor.execute(
                        f"UPDATE users SET password = '{new_password}' WHERE username = '{retrieved_username}'")
                    mydb.commit()
                    st.success("Password updated successfully!")
            except DbConnectionError as error:
                st.error(f"Failed to update password: {error}")
            finally:
                cursor.close()

    if st.checkbox('Email change'):
        if retrieved_email:
            st.subheader("Email")
            st.write(f"Current Email: {retrieved_email}")
            new_email = st.text_input("New Email:")
            if st.button("Update Email"):
                try:
                    cursor = mydb.cursor()
                    cursor.execute(f"UPDATE users SET email = '{new_email}' WHERE email = '{retrieved_email}'")
                    mydb.commit()
                    st.success("Email updated successfully!")
                except DbConnectionError as error:
                    st.error(f"Failed to update email: {error}")
                finally:
                    cursor.close()

    mydb.close()













import streamlit as st

from utils import *

import login

from sqlalchemy import text

def app():

    # Initialize SQL connection.
    # Uses @st.cache_resource to run only once
    @st.cache_resource
    def init_conn():
        db_url = st.secrets["DATABASE_URL"]
        return st.connection("postgresql", type="sql", url=db_url)
    conn = init_conn()

    # Get the email of the user
    email = login.email_fn()

    st.title("Change Password")
    st.text(f"{email}")

    cur_pass = st.text_input("Current Password", type="password")
    pass1 = st.text_input("New Password", type="password")
    pass2 = st.text_input("Confirm Password", type="password")

    # Hashing the current password
    hashed_password = hash_password(cur_pass)

    # Run SQL query to get the current password of the user, i.e., the password corresponding to the email
    true_pass = conn.query(f"SELECT password FROM users WHERE email = '{email}';", ttl="10m")
    
    if not true_pass.empty:
        true_pass = true_pass.iloc[0, 0]

        if st.button("Update"):

            # Check if the current password is valid
            if hashed_password != true_pass:
                st.error("Invalid Password")
            
            # Check if new password and confirm password is same
            elif pass1 != pass2:
                st.error("Password Mismatched")

            else:
                # Hashing the new password
                hashed_password = hash_password(pass1)
                # Update the password in database
                with conn.session as session:
                    query = text(f"UPDATE users SET password = '{hashed_password}' WHERE email = '{email}';")
                    session.execute(query)
                    session.commit()
                st.success("Password Changed Successfully")
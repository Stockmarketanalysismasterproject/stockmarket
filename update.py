import streamlit as st
from sqlalchemy import text
import login
from utils import *

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

    st.title("Edit Profile")
    st.text(f"{email}")

    name = st.text_input("Edit Name")

    if st.button("Update"):

        # Update the user database
        with conn.session as session:
            query = text(f"UPDATE users SET name = '{name}' WHERE email = '{email}';")
            session.execute(query)
            session.commit()

        st.success("Profile Updated Successfully")
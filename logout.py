import streamlit as st
from sqlalchemy import text
import time

from utils import *

import login

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

    # Update the user auth_status
    with conn.session as session:
        query = text(f"UPDATE users SET login_status = 'FALSE' WHERE email = '{email}';")
        session.execute(query)
        session.commit()

    st.success("Loged Out Successfully")
    time.sleep(3)
    st.switch_page('index.py')


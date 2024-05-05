import streamlit as st
import time

from sqlalchemy import text

from utils import *

# Initialize SQL connection.
# Uses @st.cache_resource to run only once
@st.cache_resource
def init_conn():
    db_url = st.secrets["DATABASE_URL"]
    return st.connection("postgresql", type="sql", url=db_url)
conn = init_conn()

def app():
    st.title("Login to Continue ....")
    
    # Add CSS style to the buttons
    st.markdown("""
      <style>
      div.stButton {text-align:center}
      div.stButton > button:first-child {
      background-color: #0099ff;
      color:#ffffff;
      }
      div.stButton > button:hover {
      background-color: #00ff00;
      color:#ff0000;
      }
      </style>""", unsafe_allow_html=True)
    
    # Email field
    global email
    email = st.text_input("Email", type="default")

    # Password field
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In"):

        # Hashing the password
        hashed_password = hash_password(password)

        # Run SQL query to check if email and corresponding password match
        count = conn.query(f"SELECT COUNT(*) FROM users WHERE email = '{email}' AND password = '{hashed_password}';", ttl="10m")
        exists = count.iloc[0, 0]

        if bool(exists) == False: # if not match
            st.error("Invalid Credentials")
        
        else:
            # Run SQL query to get the name of the user, i.e., the name corresponding to the email
            global name
            name = conn.query(f"SELECT name FROM users WHERE email = '{email}';", ttl="10m")
            name = name.iloc[0, 0]

            # Update the user auth_status
            with conn.session as session:
                query = text(f"UPDATE users SET login_status = 'TRUE' WHERE email = '{email}';")
                session.execute(query)
                session.commit()

            st.success(f"Logged in as {name}")
            time.sleep(3)
            # Redirect to stock trend page
            st.switch_page('pages/app.py')

def email_fn():
    user_email = email
    return user_email

def name_fn():
    user_name = name
    return user_name
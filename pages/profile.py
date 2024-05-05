import streamlit as st
import time

from streamlit_option_menu import option_menu

import reset, update, login, logout
from utils import *

# Initialize SQL connection.
# Uses @st.cache_resource to run only once
@st.cache_resource
def init_conn():
    db_url = st.secrets["DATABASE_URL"]
    return st.connection("postgresql", type="sql", url=db_url)
conn = init_conn()

# Get the email of the user
email = login.email_fn()

try:
    # Run SQL query to get the login status of the user
    login_status = conn.query(f"SELECT login_status FROM users WHERE email = '{email}';", ttl="10m")
    login_status = login_status.iloc[0, 0]

    if login_status == 'TRUE':
        # Get the name of the user
        name = login.name_fn()

        class MultiApp:

            def __init__(self):
                self.apps = []

            def add_app(self, title, func):

                self.apps.append({
                    "title": title,
                    "function": func
                })

            def run():
                # Navigation sidebar
                with st.sidebar:        
                    app = option_menu(
                        menu_title='Settings',
                        options=['Edit Profile','Change Password', 'Logout'],
                        icons=['person-fill-gear','person-fill-lock', 'person-fill-dash'],
                        menu_icon='list',
                        default_index=1,
                        styles={
                            "container": {"padding": "5!important","background-color":'black'},
                "icon": {"color": "white", "font-size": "23px"}, 
                "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                "nav-link-selected": {"background-color": "#02ab21"},}               
                )

                
                if app == "Edit Profile":
                    # Call app function from update.py
                    update.app()
                if app == "Change Password":
                    # Call app function from reset.py
                    reset.app()
                if app == "Logout":
                    # Call app function from logout.py
                    logout.app()
                
            run()

except IndexError:
    st.error("Unauthorized Access. Please Login")
    time.sleep(3)
    st.switch_page('index.py')
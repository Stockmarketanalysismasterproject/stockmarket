import streamlit as st

from streamlit_option_menu import option_menu

import reset, update, logout
from utils import *

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
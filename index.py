import streamlit as st

import login
from utils import *

# Set page configuration
#st.set_page_config(page_title="Stock Trend App", page_icon="💹")

# Call app function from login.py
login.app()

col1, col2 = st.columns([1,1])  # Adjust column ratios as needed

# Add Forgot Password button
with col1:
    if st.button("Forgot Password ?", use_container_width=True):
        # Redirect to forgot password page
        st.switch_page('pages/forgot_pass.py')

# Add Sign Up button        
with col2:
    if st.button("Create An Account", use_container_width=True):
        # Redirect to sign up page
        st.switch_page('pages/signup.py')
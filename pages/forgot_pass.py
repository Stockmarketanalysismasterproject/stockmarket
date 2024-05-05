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

# Generate OTP
@st.cache_resource
def init_otp(otp_len):
    return generateOTP(otp_len)
otp = init_otp(6)

st.title("Forgot Password")

email = st.text_input("Enter Email")

# Run SQL query to check if email exist
count = conn.query(f"SELECT COUNT(*) FROM users WHERE email = '{email}';", ttl="10m")
exists = count.iloc[0, 0]


if st.button("Send OTP"):

    # Check the format of the email
    if check_email(email) == False:
        st.error("Invalid Email")

    # Check if email exist
    elif bool(exists) == False:
        st.error("User with this email was not found")
    
    # Send OTP to email
    else:
        # DEfine the email
        subject = "Password Reset OTP"
        html = f"""\
             <html>
             <body>
                 <div style="color:gray; margin:auto; font-size: 16px;">OTP for Password Reset is {otp}</div>
             </body>
             </html>
             """
        # Send the email with OTP
        sendMail(subject, email, html)   
        st.success("OTP Sent Successfully")
               
value = st.text_input("Enter OTP")

new_pass = st.text_input("Enter Password", type="password", help="Password Policy:\n    1. Minimum 8 Characters\n    2. Atleast 1 Upper Case\n    3. Atleast 1 Digit\n    4. Atleast 1 Special Character")
        
if st.button("Submit"):
        
    # Check if the password follows the defined policies
    if pass_strength(new_pass) == False:
        st.error("Weak Password")

    elif otp != value:
        st.error("Incorrect OTP")
    
    else:
        # Hashing the password
        hashed_password = hash_password(new_pass)
        # Update the user database
        with conn.session as session:
            query = text(f"UPDATE users SET password = '{hashed_password}' WHERE email = '{email}';")
            session.execute(query)
            session.commit()
        st.success("Password Changed Successfully")
        time.sleep(3)
        st.switch_page('index.py')
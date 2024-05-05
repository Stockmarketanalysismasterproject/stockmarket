import streamlit as st
import time
from sqlalchemy import text
from utils import *

from sqlalchemy.exc import IntegrityError


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

st.title("Sign Up")

name = st.text_input("Name")
email = st.text_input("Email")


if st.button("Send OTP"):
    # Define the email
    subject = "Registration OTP"
    html = f"""\
         <html>
         <body>
             <div style="color:gray; margin:auto; font-size: 16px;">OTP for Registration is {otp}</div>
         </body>
         </html>
         """
    # Send email with OTP
    sendMail(subject, email, html)
    st.success("OTP Sent Successfully")

value = st.text_input("OTP")

pass1 = st.text_input("Password", type="password", help="Password Policy:\n    1. Minimum 8 Characters\n    2. Atleast 1 Upper Case\n    3. Atleast 1 Digit\n    4. Atleast 1 Special Character")
pass2 = st.text_input("Confirm Password", type="password")

# Hashing the password
hashed_password = hash_password(pass1)

if st.button("Sign Up"):

    # Check if all fields are entered
    if name.strip() == "" or email.strip() == "" or pass1.strip() == "" or pass2.strip() == "":
        st.error("All fields are mandatory")

    # Check the format of the email
    elif check_email(email) == False:
        st.error("Invalid Email")

    # Check if the password follows the defined policies
    elif pass_strength(pass1) == False:
        st.error("Weak Password")

    # Check if password and confirm password is samee
    elif pass1 != pass2:
        st.error("Password Mismatched")
    
    # Chech if OTP is correct
    elif otp != value:
        st.error("Invalid OTP")
   
    else:
        try:
             # execute SQL Query to insert user details into database
            with conn.session as session:
                query = text(f"INSERT INTO users (email, name, password) VALUES ('{email}', '{name}', '{hashed_password}');")
                session.execute(query)
                session.commit()
            st.success("Account Created Successfully")
            time.sleep(3)
            st.switch_page('index.py')

            # Define the email
            subject = "Registration Successed in Stock Trend"
            html = f"""\
                    <html>
                    <body>
                        <div style="color:blue; margin:auto; font-size: 20px; font-weight:bold">Welcome to Stock Trend</div>
                        <div style="color:gray; font-size: 16px">Hi {name}<br>Now you can login into your account.<br>Enjoy It!</div>
                    </body>
                    </html>
                    """
            # Send email
            sendMail(subject, email, html)

        except IntegrityError as e:
            # IntegrityError Exception: This exception is raised when the relational integrity of the data is affected.
            # For example, a duplicate key was inserted or a foreign key constraint would fail.
            # Email is primary key
            st.error("Email already exists!")
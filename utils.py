import string, secrets
import streamlit as st
import os

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait

import re

from password_strength import PasswordPolicy

import hashlib

# Define a function for send email
def sendMail(subject, receiver_email, html_message):
    def sendMail_fun(**kwargs):

        sender_email = st.secrets["SENDER_EMAIL"]
        receiver_email = kwargs['receiver_email']
        username = st.secrets["EMAIL_USERNAME"]
        password = st.secrets["EMAIL_PASSWORD"]

        message = MIMEMultipart()
        message["Subject"] = kwargs['subject']
        message["From"] = sender_email
        message["To"] = receiver_email
        
        print(receiver_email)
        print(message["Subject"])

        # Create the plain-text and HTML version of your message
        html = kwargs['html_message']

        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        # ssl._create_default_https_context = ssl._create_unverified_context
        context = ssl.create_default_context()
        # server = smtplib.SMTP_SSL("smtp.sendgrid.net", 465, context=context)
        server = smtplib.SMTP(st.secrets["EMAIL_HOST"], 587)
        server.set_debuglevel(True)
        server.starttls(context=context) # Secure the connection
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        res = server.sendmail(sender_email, receiver_email, message.as_string())
        print(res)
        server.quit()
    kwargs = locals()
    try:
        #executor = ThreadPoolExecutor()
        #future = executor.submit(sendMail_fun, **kwargs)
        #executor.shutdown(wait=False)
        sendMail_fun(**kwargs)
    except Exception as e:
        pass



# Define a function for generate OTP
def generateOTP(length :int):
    e = string.digits
    otp = ''.join([secrets.choice(e) for i in range(length)])
    return otp


# Define a function for validating an Email
def check_email(email):

    # Make a regular expression
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False
    


# Define a function for password hashing
def hash_password(password):
    # adding salt
    salt = st.secrets["HASH_SALT"]

    # Adding salt at the last of the password
    dataBase_password = password+salt
    # Encoding the password
    hashed = hashlib.md5(dataBase_password.encode())

    # return the hashed password
    return hashed.hexdigest()



# Define a function for check the password strength
def pass_strength(password):
    policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1,  # need min. 1 special characters
    )
    lis = policy.test(password)

    if len(lis) == 0:
        return True
    else:
        return False
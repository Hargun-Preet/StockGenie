import streamlit as st
from db import login_user, register_user, generate_reset_token, verify_reset_token, reset_password, is_registered_user, update_user, clear_reset_token
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

def is_password_valid(password):
    """
    Validates password strength.
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must include at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must include at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must include at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must include at least one special character."
    return True, ""

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def send_reset_email(email, token):
    sender_email = "hargunpreet177@gmail.com"  # Replace with your email
    sender_password = "qggz mbck ptif ijzl"      # Replace with your email password
    receiver_email = email
    reset_link = token  # Token is shown to the user as no page redirect

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Hi, \nYour token to reset your password is: {reset_link}"
    html = f"""\

    <html>
      <body>
        <p>Hi,<br>
           Your token to reset your password is: {reset_link}
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    # Send the email
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        st.success(f"A reset token has been sent to {email}. Please check your inbox.")
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")




def login_page():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "forgot_password" not in st.session_state:
        st.session_state["forgot_password"] = False
    if "sent_reset_token" not in st.session_state:
        st.session_state["sent_reset_token"] = False

    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["user"] = user
                st.success(f"Welcome, {user['username']}!")
            else:
                st.error("Invalid username or password")
                st.session_state["forgot_password"] = True  # Set flag to True on login failure

    # Forgot Password section
    if st.button("Forgot Password?") or st.session_state["forgot_password"]:
        st.session_state["forgot_password"] = True  # Keep the section open
        with st.expander("Reset Password"):
            email = st.text_input("Enter your registered email")
            
            # Send reset token
            if st.button("Send Reset Link"):
                if not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                elif is_registered_user(email):
                    token = generate_reset_token(email)
                    send_reset_email(email, token)
                    if token:
                        st.success("Password reset link has been sent to your email.")
                        st.session_state["sent_reset_token"] = True
                    else:
                        st.error("Error generating reset token.")
                else:
                    st.error("This email is not registered.")


        # Input fields for reset token and new password
        if st.session_state["sent_reset_token"]:
            st.write("### Reset Password (after receiving token)")
            token_input = st.text_input("Enter reset token")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            # Button to reset the password after token validation
            if st.button("Reset Password"):
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    valid, message = is_password_valid(new_password)
                    if not valid:
                        st.error(message)
                    else:
                        if verify_reset_token(email, token_input):
                            reset_password(email, new_password)
                            clear_reset_token(email)
                            st.success("Password reset successfully. You can now log in.")
                            st.session_state["forgot_password"] = False
                            st.session_state["sent_reset_token"] = False
                        else:
                            st.error("Invalid token.")




# Register Page
def register_page():
    st.subheader("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            valid, message = is_password_valid(password)
            if not valid:
                st.error(message)
            else:
                if register_user(username, email, password):
                    st.success("Registration successful. Please log in.")
                else:
                    st.error("User already exists. Please log in.")



def update_profile():
    st.subheader("Update Profile")
    user = st.session_state["user"]

    # Pre-fill the current username and email
    new_username = st.text_input("New Username", value=user['username'])
    new_email = st.text_input("New Email", value=user['email'])
    new_password = st.text_input("New Password", type="password", placeholder="Leave blank if you don't want to change it")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Leave blank if you don't want to change it")
    
    if st.button("Save Changes"):
        if new_username != user['username']:
            update_user(user['username'], new_username=new_username)
            st.success("Username updated successfully.")
        
        if new_email != user['email']:
            if not is_valid_email(new_email):
                st.error("Please enter a valid email address.")
            else:
                update_user(user['username'], new_email=new_email)
                st.success("Email updated successfully.")
        
        if new_password:  # Only validate if a new password is provided
            if new_password != confirm_password:
                st.error("Passwords do not match. Try again.")
            else:
                valid, message = is_password_valid(new_password)
                if not valid:
                    st.error(message)
                else:
                    reset_password(user['email'], new_password)  # Use user['email'] instead of user['username']
                    st.success("Password updated successfully.")
    
        # Update session state with new details
        user['username'] = new_username
        user['email'] = new_email




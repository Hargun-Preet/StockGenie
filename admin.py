# admin.py
import streamlit as st
from db import view_all_users, update_user, delete_user
import re

# Email validation
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def admin_dashboard():
    st.title("Admin Dashboard")
    st.write("View and manage all users")

    # Display users
    all_users = view_all_users()
    st.table(all_users)

    # Form to update users
    st.subheader("Update Any Profile")
    username_to_update = st.text_input("Username to update")
    new_email = st.text_input("New email (optional)")
    new_username = st.text_input("New username (optional)")
    
    if st.button("Update User"):
        if new_email and not is_valid_email(new_email):
            st.error("Please enter a valid email address.")
        else:
            update_user(username_to_update, new_email, new_username)
            st.success(f"Updated user {username_to_update}")

    # Delete user functionality
    st.subheader("Delete Any Profile")
    username_to_delete = st.selectbox("Select a user to delete", [user['username'] for user in all_users])
    
    if st.button("Delete User"):
        if username_to_delete:
            delete_user(username_to_delete)
            st.success(f"User {username_to_delete} has been deleted.")


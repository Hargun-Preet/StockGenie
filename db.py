from pymongo import MongoClient
import bcrypt
import uuid
from datetime import datetime, timedelta

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["StockPrediction"]
users_collection = db["StockPrediction"]  # Corrected collection name to "Users"

# Function to register a user
def register_user(username, email, password, role='user'):
    # Check if user is already registered
    if users_collection.find_one({"email": email}):
        return False  # User already exists
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password,
        "role": role,
        "reset_token": None,
        "token_expiration": None
    })
    return True

# Function to check if login credentials are valid
def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user
    return None

# Function to check if a user is registered by email
def is_registered_user(email):
    user = users_collection.find_one({"email": email})
    return user is not None

# Function to view all users (Admin functionality)
def view_all_users():
    return list(users_collection.find({}, {"_id": 0, "username": 1, "email": 1}))

# Function to delete a user
def delete_user(username):
    users_collection.delete_one({"username": username})

# Function to update user details (Admin functionality)
def update_user(username, new_email=None, new_username=None):
    update_fields = {}
    if new_email:
        update_fields["email"] = new_email
    if new_username:
        update_fields["username"] = new_username
    users_collection.update_one({"username": username}, {"$set": update_fields})

# Reset password for a user
def reset_password(email, new_password):
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})

# Generate a password reset token for a user
def generate_reset_token(email):
    user = users_collection.find_one({"email": email})
    if not user:
        return None  # User not found

    token = str(uuid.uuid4())  # Generate a unique token
    expiration_time = datetime.now() + timedelta(minutes=10)  # Token valid for 10 minutes
    users_collection.update_one(
        {"email": email},
        {"$set": {"reset_token": token, "token_expiration": expiration_time}}
    )
    return token

# Verify if the reset token is valid
def verify_reset_token(email, token):
    user = users_collection.find_one({
        "email": email,
        "reset_token": token,
        "token_expiration": {"$gt": datetime.now()}
    })
    return user is not None

# Clear the reset token after successful password reset
def clear_reset_token(email):
    users_collection.update_one(
        {"email": email},
        {"$unset": {"reset_token": "", "token_expiration": ""}}
    )

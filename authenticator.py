import hashlib
import os
import re
from controllers import database_controller

db_controller = database_controller.DatabaseController()

def validate_email(email):
    pattern = r'^[A-Za-z]+\.[A-Za-z]+@university\.com$'
    return re.match(pattern, email)

def validate_password(password):
    pattern = r'^[A-Z][A-Za-z]{4,}\d{3,}$'
    return re.match(pattern, password)

def hash_password(password):
    salt = os.urandom(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return (salt + pwd_hash).hex()

def verify_password(stored_hash, password):
    try:
        salt = bytes.fromhex(stored_hash[:64])
        stored_pwd_hash = bytes.fromhex(stored_hash[64:])
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return pwd_hash == stored_pwd_hash
    except:
        return False

def authenticate(email, password):
    stored_hash = db_controller.get_password(email)
    if stored_hash is None:
        return False
    return verify_password(stored_hash, password)
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
import jwt
import time
from decouple import config
from models.user import *
from .jwt_handler import decodeJWT

# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
# ALGORITHM = "HS256"
# JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
# JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_hashed_password(password: str) -> str:
#     return password_context.hash(password)


# def verify_password(password: str, hashed_pass: str) -> bool:
#     return password_context.verify(password, hashed_pass)

# def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
        
#     else:
#         expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
         
    
#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
#     return encoded_jwt

# def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
#     return encoded_jwt

JWT_SECRET = config("secret", default='default_value')
JWT_ALGORITHM = config("algorithm", default="HS256")
# Function returns the generated Tokens (JWT's)
def token_response(token: str):
    return {
        "access token" : token
    }
# Function uses for signing the JWT string    
def signJWT(userId : str):
    payload = {
        "userId" : userId,
        "expiry" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token : str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm = JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}
    

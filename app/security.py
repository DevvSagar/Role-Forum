from fastapi import HTTPException
from pwdlib import PasswordHash
from jose import JWTError , jwt
from app.config import get_app_config
from datetime import datetime , timedelta , timezone



def HashPassword(password: str) -> str:
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)


def VerifyPassword(password : str , hashed_password : str) -> bool:
   password_hash = PasswordHash.recommended()
   return password_hash.verify(password , hashed_password)

def create_access_token(data : dict) -> str:
    config = get_app_config()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)

def verify_token(token:str):
    config = get_app_config()
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
from fastapi import Depends
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security import verify_token

security_scheme = HTTPBearer()


def authenicate_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)]):
    token = credentials.credentials
    decoded = verify_token(token)
    return decoded
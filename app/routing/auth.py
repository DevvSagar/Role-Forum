from fastapi import APIRouter , Depends , HTTPException
from app.database.db import get_db
from app.models.user import UserModel
from app.schemas.user import Login , Register
from typing import Annotated
from sqlalchemy.orm import Session
from app.security import VerifyPassword , HashPassword , create_access_token
from app.dependencies import authenicate_user




router = APIRouter(prefix="/role/auth")

@router.post("/login")
def Login(data : Login , db:Annotated[Session , Depends(get_db)]):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401 , detail="User not Found !!!")

    if not VerifyPassword(data.password , user.password):
        raise HTTPException(status_code=401 , detail="Wrong Credentials !!!")

    token = create_access_token({"sub": user.email})

    return{
        "Message" : "Logged In...",
        "Token" : token,
        "token_type": "bearer"
    }


@router.post("/register")
def Register(data : Register , db:Annotated[Session , Depends(get_db)]):
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=401 , detail="User Already Defined !!!")

    new_user = UserModel(
        name = data.name,
        email = data.email,
        password = HashPassword(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{
        "Message" : "User Registered"
    }

@router.get("/profile")
def get_profile(db:Annotated[Session , Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()

    if not user:
        raise HTTPException(status_code=401 , detail="User not Found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
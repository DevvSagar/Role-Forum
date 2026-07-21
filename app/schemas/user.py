from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo

class Login(BaseModel):
    email : EmailStr
    password : str = Field(min_length=8 , max_length=100)


class Register(BaseModel):
    name : str = Field(min_length=1 , max_length=50)
    email : EmailStr
    password : str = Field(min_length=8 , max_length=100)
    confirm_password : str = Field(min_length=8,max_length=100)

    @field_validator("confirm_password")
    @classmethod
    def passwordchecker(cls , confirm_password , information:ValidationInfo):
        password = information.data.get("password")
        if password == confirm_password:
            return confirm_password
        raise ValueError("Password Didnt Match !!!")


from pydantic import BaseModel , Field
from typing import Optional

class CreateComment(BaseModel):
    content : str = Field(max_length=500 , min_length=5)

class UpdateComment(BaseModel):
    content : Optional[str] = Field(max_length=500, min_length=5 , default=None)
from pydantic import BaseModel , Field
from typing import Optional

class CreatePost(BaseModel):
    title : str = Field(max_length=500, min_length=5)
    content : str = Field(max_length=500, min_length=5)

class UpdatePost(BaseModel):
    title : Optional[str] = Field(max_length=500, min_length=5 , default=None)
    content : Optional[str] = Field(max_length=500, min_length=5 , default=None)
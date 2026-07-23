from pydantic import BaseModel , Field

class CreateComment(BaseModel):
    comment : str = Field(max_length=500 , min_length=5)
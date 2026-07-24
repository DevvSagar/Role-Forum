from fastapi import APIRouter , Depends , HTTPException
from app.database.db import get_db
from app.schemas.comment import CreateComment , UpdateComment
from app.models.comment import CommentModel
from app.models.user import UserModel
from app.models.post import PostModel
from typing import Annotated
from sqlalchemy.orm import Session
from app.dependencies import authenicate_user



router = APIRouter(prefix="/comment")


@router.get("/{id}")
def all_comments(id : int , db : Annotated[Session , Depends(get_db)]):
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post:
        raise HTTPException(status_code=403 , detail="Posts didn't Found !!!")

    comment = db.query(CommentModel).filter(CommentModel.post_id == id).all()
    return{"Commments" : comment}


@router.post("/createComment/{post_id}")
def create_comment(post_id : int , data : CreateComment , db: Annotated[Session , Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=401 , detail="User not Found !!")

    create_comment = CommentModel(
        content = data.content,
        post_id = post_id,
        author_id = user.id
    )

    db.add(create_comment)
    db.commit()
    db.refresh(create_comment)

    return{"Message" : "Comment Created !!"}


@router.put("/UpdateComment/{id}")
def edit_comments(id : int ,  data:UpdateComment , db: Annotated[Session , Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=401 , detail="User not Found !!")

    comments = db.query(CommentModel).filter(CommentModel.id == id).first()

    if comments.author_id == user.id or user.role == "admin":
        comments.content = data.content
        db.commit()
        db.refresh(comments)
    else:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comments")

    return{"Message" : "Comment Updated !!"}

@router.delete("/DeleteComments/{id}")
def delete_Comments(id : int ,  db: Annotated[Session , Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=401 , detail="User not Found !!")

    comments = db.query(CommentModel).filter(CommentModel.id == id).first() 
    
    if comments.author_id == user.id or user.role == "admin":
        db.delete(comments)
        db.commit()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to Delete this comments")
    
    return{"Message" : "Comment Deleted !!"}
    
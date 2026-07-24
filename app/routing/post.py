from fastapi import APIRouter , Depends , HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.post import PostModel
from sqlalchemy import select 
from app.dependencies import authenicate_user
from app.schemas.post import CreatePost , UpdatePost
from app.models.user import UserModel

router = APIRouter(prefix="/post")


@router.get("/")
def all_posts(db:Annotated[Session , Depends(get_db)]):
    stmt = select(PostModel.id , PostModel.title , PostModel.content)
    post = db.execute(stmt).mappings().all()

    return {"Posts": post}

@router.get("/{id}")
def post_by_id(id : int , db:Annotated[Session , Depends(get_db)]):
    stmt = select(PostModel.id , PostModel.title , PostModel.content).filter(PostModel.id == id)
    post = db.execute(stmt).mappings().all()

    if not post:
        raise HTTPException(status_code=403 , detail="Id is Invalid !!!")
    
    return {"Posts": post}

@router.post("/createPost")
def create_posts(data : CreatePost , db:Annotated[Session , Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=403 , detail="User not Found !!")

    new_post = PostModel(
        title = data.title,
        content = data.content,
        author_id = user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return{
        "Message" : "Post Created",
        "Post" : new_post
    }

@router.put("/editPost/{id}")
def edit_post( data : UpdatePost , id : int , db:Annotated[Session , Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user :
        raise HTTPException(status_code=403 , detail="User not Found !!")

    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post :
        raise HTTPException(status_code=403 , detail="Post not Found !!")


    if post.author_id == user.id or user.role == "admin":
        post.title = data.title
        post.content = data.content
        db.commit()
        db.refresh(post)
    else:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")

    return{
        "Message" : "Post Updated !!"
    }

@router.delete("/deletePost/{id}")
def delete_post(id : int , db:Annotated[Session , Depends(get_db)] , current_user : Annotated[dict , Depends(authenicate_user)]):
    user = db.query(UserModel).filter(UserModel.email == current_user["sub"]).first()
    if not user :
        raise HTTPException(status_code=403 , detail="User not Found !!")
    post = db.query(PostModel).filter(PostModel.id == id).first()
    if not post :
        raise HTTPException(status_code=403 , detail="Post not Found !!")
    
    if post.author_id == user.id or user.role == "admin":
        db.delete(post)
        db.commit()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")

    return{"Message" : "Post Deleted !!"}
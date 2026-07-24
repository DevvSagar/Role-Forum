from fastapi import FastAPI
from app.routing import auth , post , comment


app = FastAPI(title="RoleForum")

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)

@app.get("/")
def root():
    return{ "Message" : "API is Running !!!"}
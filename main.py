from fastapi import FastAPI
from app.routing import auth


app = FastAPI(title="RoleForum")

app.include_router(auth.router)

@app.get("/")
def root():
    return{ "Message" : "API is Running !!!"}
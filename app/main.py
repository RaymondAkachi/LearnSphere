from fastapi import FastAPI
from app.routes import users, content
from app.database import init_db

app = FastAPI(title="LeanSphere - Oflline Learning App")

# Initialize the database
init_db()

# Include routers
app.include_router(users.router, prefix="/users")
app.include_router(content.router, prefix="/content")


@app.get("/")
def read_root():
    return {"message": "Welcome to LearnSphere!"}

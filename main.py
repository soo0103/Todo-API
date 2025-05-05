from fastapi import FastAPI
from models import Base
from database import engine
from routers import todo

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(todo.router)


@app.get("/")
def read_root():
    return "🎉 Welcome to the FastAPI Todo API!"

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://velog.io/@nemo-cat/todolist
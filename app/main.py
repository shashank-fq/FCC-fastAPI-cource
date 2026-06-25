from fastapi import FastAPI, Response, HTTPException, status, Depends
# from fastapi.params import Body
# from pydantic import BaseModel

# from typing import Optional,List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models, schemas, utils
from .config import settings
from .database import engine, SessionLocal, get_db
# from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# while(1):
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'FastAPI database', user = 'postgres', password = 'dhisdat', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#             {"title": "title of post 2", "content": "content of post 2", "id": 2},
#             {"title": "post 3", "content": "content 3", "id": 3}
#             ]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "hello fastAPI"}



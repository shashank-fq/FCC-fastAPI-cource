from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
# from fastapi.params import Body
# from pydantic import BaseModel
from typing import List, Optional
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from sqlalchemy import func
from .. import models, schemas, oauth2
# from . import router
from ..database import get_db
from sqlalchemy.orm import Session
# models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix = "/posts",
    tags=['Posts'] 
)


@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              Limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # print(Limit)
    
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(
        # models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).filter(
    models.Post.title.contains(search)).limit(Limit).offset(skip).all()


    # posts = db.query(models.Post).limit(Limit).offset(skip).all()

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(current_user.id)
    # print(posts)
    return posts
    


# @router.post("/", status_code = status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     # print(post)
#     # print(post.dict())
#     # post_dict = post.dict()
#     # post_dict['id'] = randrange(0, 100000)
#     # my_posts.routerend(post_dict)
#     # my_posts.routerend(post,dict())

#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,
#                     (post.title, post.content, post.published))
#     new_post = cursor.fetchone()

#     conn.commit()
#     return {"data": new_post}
#title str, content str

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
    ):

    # print(current_user)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @router.get("//{id}")
# def get_post(id: int, response: Response):
#     cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
#     post = cursor.fetchone()
#     # print(post)
#     # post = find_post(id)
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id: {id} was not found")
#         # response.status_code = 404
#         # return{'message': f"post with id: {id} was not found"}
#     # print(post)
#     return{"post_detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")

    return post


# @router.delete("//{id}", status_code = status.HTTP_201_CREATED)
# def delete_post(id: int):
# #find the index in the array
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()

#     # index = find_index_post(id)
#     if deleted_post == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id: {id} was not found")
        

#     # my_posts.pop(index)
#     return Response(status_code = status.HTTP_204_NO_CONTENT)
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # post = post_query.first()

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("//{id}")
# def update_post(id: int, post: Post):
#     # index = find_index_post(id)
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING * """, 
#                    (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id: {id} does not exist")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # print(post)
    # return {"data": updated_post}

@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
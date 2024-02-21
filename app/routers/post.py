from app import models, schemas, utils
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from typing import List


router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

# Returns all the posts 
@router.get("/", response_model=List[schemas.PostResponse])
def get_post(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# # Returns the latest post 
# @router.get("/latest")
# def get_latest_post():
#     cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
#     new_post = cursor.fetchone()
#     return new_post


# Returns post with id 
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id:int ,db:Session = Depends(get_db)):
    
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s)""", (post.title, post.content, post.published))
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    # del_post = cursor.fetchone()
    # cursor.execute(f"""DELETE FROM posts WHERE id = {id}""")
    # mydb.commit()
    
    del_post = db.query(models.Post).filter(models.Post.id == id)
    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    del_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db:Session = Depends(get_db)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s""", (post.title, post.content, post.published, str(id)))
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    # updated_post = cursor.fetchone()
    # mydb.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updatepost = post_query.first()
    if updatepost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
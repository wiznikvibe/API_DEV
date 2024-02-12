from fastapi import FastAPI , Response, status, HTTPException, Depends
from fastapi.params import Body

from typing import Optional
from random import randrange
import mysql.connector as conn
from sqlalchemy.orm import Session
from configparser import ConfigParser
import time
from app import models, schemas
from app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



config = ConfigParser()
config.read('config.ini')

host = config['USER']['host']
user = config['USER']['user']
password = config['USER']['password']
database = config['USER']['database']

while True:
    try:
        mydb = conn.connect(host=host, user=user, password=password, database=database)
        cursor = mydb.cursor(buffered=True, dictionary=True)
        # tables = cursor.execute("""SHOW TABLES;""")
        print("Connection Succefully Established")
        # print(tables)
        break
    except Exception as e:
        print("Connection Failed")
        print("Error:", e)
        time.sleep(2)


@app.get("/")
def root():
    return {"message":"Hello World !"}



# Returns all the posts 
@app.get("/posts")
def get_post(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

# Returns the latest post 
@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    new_post = cursor.fetchone()
    return {"data":new_post}

# 5:16:03
# Returns post with id 
@app.get("/posts/{id}")
def get_post(id:int ,db:Session = Depends(get_db)):
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {"post details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s)""", (post.title, post.content, post.published))
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@app.put('/posts/{id}')
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

    return {'data':post_query.first()}


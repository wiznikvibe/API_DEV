from fastapi import FastAPI , Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import mysql.connector as conn
import psycopg2
from psycopg2.extras import RealDictCursor
from configparser import ConfigParser
import time

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

# Class for Base Model 
class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    

# ### Sample Posts
# my_posts = [{"title":"title of Post 1","content":"content of Post 1","id": 1},{"title":"title of Post 2","content":"content of Post 2","id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p 
    
def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 



@app.get("/")
def root():
    return {"message":"Hello World !"}

# Returns all the posts 
@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# Returns the latest post 
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[int(len(my_posts)-1)]
    return {"data":post}

# Returns post with id 
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    # print(post)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {"post details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,10000)
    # my_posts.append(post_dict)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s)""", (post.title, post.content, post.published))
    cursor.execute("""SELECT LAST_INSERT_ID() as inserted_id""")
    new_post = cursor.fetchone()
    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete posts 
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict


    return {'message':f'{post_dict} Updated'}


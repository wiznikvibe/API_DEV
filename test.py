from fastapi import FastAPI , Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Class for Base Model 
class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

### Sample Posts
my_posts = [{"title":"title of Post 1","content":"content of Post 1","id": 1},{"title":"title of Post 2","content":"content of Post 2","id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p 


@app.get("/")
def root():
    return {"message":"Hello World !"}

# Returns all the posts 
@app.get("/posts")
def get_post():
    return {"data": my_posts}

# Returns the latest post 
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[int(len(my_posts)-1)]
    return {"data":post}

# Returns post with id 
@app.get("/posts/{id}")
def get_post(id: int, response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')
    return {"post details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"data": post_dict}

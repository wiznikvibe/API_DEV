from pydantic import BaseModel


# Class for Base Model 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass 

class PostUpdate(PostBase):
    pass 
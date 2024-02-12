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

class PostResponse(PostBase):
    title: str
    content: str
    published: bool

    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import datetime

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
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

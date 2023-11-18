from pydantic import BaseModel
from uuid import UUID
from typing import List,Optional

class AddGraduate(BaseModel):
    graduate_name: str

class ReturnGraduate(BaseModel):
    graduate_name: str
    picture_name: str
    picture_link: str

class Graduates(BaseModel):
    picture_name: str
    graduate_name: str
    
    class Config:
        orm_mode = True
        
class Comment(BaseModel):
    name_of_commenter: str
    comment: str
    
    class Config:
        orm_mode = True

class ReturnComment(BaseModel):
    name_of_commenter: str
    comment: str
    graduate_id: UUID
    
    class Config:
        orm_mode = True

class AddComment(BaseModel):
    name_of_commenter: str
    comment: str
    graduate_id: UUID
    
    class Config:
        orm_mode = True
        
class GraduatesWithComments(BaseModel):
    id: UUID
    graduate_name: str
    picture_name: str
    picture_link: str
    comments: Optional[List[Comment]] = None
    
class PaginatedGraduatesWithComments(BaseModel):
        graduates: Optional[List[GraduatesWithComments]] = None
        pagination_url: Optional[str] = None
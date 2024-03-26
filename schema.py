from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class AddGraduate(BaseModel):
    graduate_name: str


class ReturnGraduate(BaseModel):
    graduate_name: str
    graduate_year: str
    graduate_description: Optional[str] = None
    picture_name: str
    picture_link: str


class Comment(BaseModel):
    name_of_commenter: str
    comment: str

    class Config:
        from_attributes = True


class ReturnComment(BaseModel):
    name_of_commenter: str
    comment: str
    graduate_id: UUID

    class Config:
        from_attributes = True


class AddComment(BaseModel):
    name_of_commenter: str
    comment: str
    graduate_id: UUID

    class Config:
        from_attributes = True


class GraduatesWithComments(BaseModel):
    id: UUID
    graduate_name: str
    graduate_year: str
    graduate_description: Optional[str] = None
    picture_name: str
    picture_link: str
    comments: Optional[List[Comment]] = None


class PaginatedGraduatesWithComments(BaseModel):
    graduates: Optional[List[GraduatesWithComments]] = None
    pagination_url: Optional[str] = None

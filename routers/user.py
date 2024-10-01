import os
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile
from database import get_db
from sqlalchemy.orm import Session
from crud import User as UserCrud
from schema import (
    AddComment,
    GraduatesWithComments,
    PaginatedGraduatesWithComments,
    ReturnComment,
    ReturnGraduate,
)
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

secret_key_access = os.environ.get("SECRET_KEY_ACCESS")

router = APIRouter(tags=["User"], prefix="/user")


@router.post(
    "/add-picture",
    status_code=status.HTTP_201_CREATED,
    response_model=ReturnGraduate,
    summary="This route is used to add a new picture of a graduate.",
    description="It allows for only one picture to be added ata time.",
)
async def upload_graduation_picture(
    graduate_name: str,
    graduate_year: str,
    graduate_picture: UploadFile,
    graduate_description: Optional[str] = None,
    api_access_code: str = Query(
        None, description="Special Key needed in order to have access to use the API"
    ),
    db: Session = Depends(get_db),
):
    graduate = {}
    resp = UserCrud.check_secret_key(api_access_code, secret_key_access)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized"
        )
    graduate["graduate_name"] = graduate_name
    graduate["picture"] = graduate_picture
    graduate["graduate_year"] = graduate_year
    graduate["graduate_description"] = graduate_description
    resp = await UserCrud.add_graduate(db, graduate)
    if resp == "Fail-D":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add Graduate Picture to Database",
        )
    if resp == "Fail-A":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add Graduate Picture to AWS Bucket",
        )
    return resp


@router.post(
    "/add-comment",
    status_code=status.HTTP_201_CREATED,
    response_model=ReturnComment,
    summary="This route enables new comments to be added to any picture of a graduate.",
    description="It returns the comment that was just sent as a response.",
)
def comment_on_a_picture(
    comment: AddComment,
    api_access_code: str = Query(
        None, description="Special Key needed in order to have access to use the API"
    ),
    db: Session = Depends(get_db),
):
    resp = UserCrud.check_secret_key(api_access_code, secret_key_access)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized"
        )
    resp = UserCrud.add_comments(db, comment)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not add Comment"
        )
    return resp


@router.get(
    "/get-hero-section-graduate-pictures",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=List[ReturnGraduate],
    summary="This route is used to get five random pictures from all graduates for a hero section.",
    description="It only returns 5 random results each time it is hit.",
)
def get_graduate_pictures_for_hero_section(
    api_access_code: str = Query(
        None, description="Special Key needed in order to have access to use the API"
    ),
    db: Session = Depends(get_db),
):
    resp = UserCrud.check_secret_key(api_access_code, secret_key_access)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized"
        )
    pictures = UserCrud.get_five_random_graduates(db)
    return pictures


@router.get(
    "/get-all-graduate-pictures-paginated",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=PaginatedGraduatesWithComments,
    summary="This route is used to get the pictures of graduates along with three comments each.",
    description="It is paginated, meaning it returns the data by pages, with 10 graduates per page.",
)
def get_all_graduate_pictures_with_comments_preview_paginated_view(
    page: Optional[int] = 1,
    api_access_code: str = Query(
        None, description="Special Key needed in order to have access to use the API"
    ),
    db: Session = Depends(get_db),
):
    resp = UserCrud.check_secret_key(api_access_code, secret_key_access)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized"
        )
    pictures = UserCrud.get_graduates_with_comments_paginated(
        api_access_code, db, items_per_page=10, page=page
    )
    return pictures


@router.get(
    "/get-comments",
    status_code=status.HTTP_200_OK,
    response_model=GraduatesWithComments,
    summary="This route is used to get all the comments under a specific picture of a graduate.",
    description="It returns a List of Json data.",
)
def get_comments_for_a_picture(
    graduate_id: UUID,
    api_access_code: str = Query(
        None, description="Special Key needed in order to have access to use the API"
    ),
    db: Session = Depends(get_db),
):
    resp = UserCrud.check_secret_key(api_access_code, secret_key_access)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized"
        )
    comments = UserCrud.get_all_picture_comments(db, graduate_id)
    return comments


@router.get(
    "/filter-graduates-by-year/{year}",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedGraduatesWithComments,
    summary="This route is used to get all the pictures of graduates in a specific year.",
    description="It returns a List of Json data.",
)
def get_pictures_of_graduates_by_year(
    year: str,
    page: Optional[int] = 1,
    api_access_code: str = Query(
        None, description="Special Key needed in order to have access to use the API"
    ),
    db: Session = Depends(get_db),
):
    resp = UserCrud.check_secret_key(api_access_code, secret_key_access)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized"
        )
    pictures = UserCrud.get_graduates_with_comments_by_year_paginated(
        api_access_code, year, db, items_per_page=10, page=page
    )
    return pictures


@router.get(
    "/search-graduates-by-name/{name}",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedGraduatesWithComments,
    summary="This route is used to get all the pictures of graduates by name.",
    description="It returns a List of Json data.",
)
def search_for_graduate_pictures_by_name(
    name: str,
    page: Optional[int] = 1,
    api_access_code: str = Query(
        None, description="Special Key needed in order to have access to use the API"
    ),
    db: Session = Depends(get_db),
):
    resp = UserCrud.check_secret_key(api_access_code, secret_key_access)
    if resp == "Fail":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized"
        )
    pictures = UserCrud.get_graduates_with_comments_by_name_paginated(
        api_access_code, name, db, items_per_page=10, page=page
    )
    return pictures

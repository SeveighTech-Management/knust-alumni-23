from uuid import UUID, uuid4
from fastapi_sqlalchemy import db
from werkzeug.utils import secure_filename
from aws import get_files, send_files
from schema import AddComment, AddGraduate
from models import Comments, Graduates
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from dotenv import load_dotenv



load_dotenv(dotenv_path ='.env')


class User():
    async def add_graduate(db: Session, graduate):
        try:
            filename = secure_filename(graduate['picture'].filename)
            unique_filename = str(uuid4())
            image_filename = unique_filename + filename[-4:]
            image_binary=await graduate['picture'].read()
            send_files(image_binary, "knustalumni23/" + image_filename, graduate['picture'].content_type)
        except Exception as e:
            print(e)
            return "Fail-A"
        
        try:
            pic = {"graduate_name": graduate['graduate_name'], "picture_name":image_filename}
            pic_to_send = Graduates(**pic)
            db.add(pic_to_send)
            db.commit()
            db.refresh(pic_to_send)
        except Exception as e:
            print(e)
            return "Fail-D"
        
        graduate_id = pic_to_send.id
        picture_details = User.get_graduate_pictures(db, graduate_id)
        return picture_details
        
    def add_comments(db: Session, comment: AddComment):
        try:
            comment_dict = comment.__dict__
            comment_to_send = Comments(**comment_dict)
            db.add(comment_to_send)
            db.commit()
            db.refresh(comment_to_send)
            return comment_to_send
        except Exception as e:
            print(e)
            return "Fail"
        
    def get_graduate_pictures(db: Session, graduate_id: UUID):
        picture = db.query(Graduates).filter(Graduates.id == graduate_id).first()
        if picture is None:
            return "E"
        picture_dict = picture.__dict__
        folder = "knustalumni23/"
        details = {"id": picture_dict['id'], "graduate_name": picture_dict["graduate_name"], "picture_name": picture_dict['picture_name'], "picture_link":""}
        if details["picture_name"] is not None:
            file_name = details["picture_name"]
            details["picture_link"] = get_files(f"{folder}{file_name}")
        return details
    
    def get_all_picture_comments(db: Session, graduate_id: UUID):
        return_comments = []
        comments = db.query(Comments).filter(Comments.graduate_id == graduate_id).all()
        for comment in comments:
            comment_dict = comment.__dict__
            return_comments.append(comment_dict)
        return return_comments
    
    def get_picture_comments_limited(db: Session, graduate_id: UUID):
        return_comments = []
        comments = db.query(Comments).filter(Comments.graduate_id == graduate_id).limit(3).all()
        for comment in comments:
            comment_dict = comment.__dict__
            return_comments.append(comment_dict)
        return return_comments
    
    def check_secret_key(db: Session, secret_key: str, SECRET_KEY_ACCESS: str):
        if secret_key != SECRET_KEY_ACCESS:
            return "Fail"
        
    def get_all_graduates_with_comments(db: Session):
        return_graduates = []
        graduates = db.query(Graduates).order_by(func.random()).all()

        for graduate in graduates:
            graduate_dict = graduate.__dict__
            graduate_id = graduate_dict["id"]
            graduate_dict_final = User.get_graduate_pictures(db=db, graduate_id=graduate_id)
            graduate_dict_final["comments"] = User.get_picture_comments_limited(db, graduate_id)
            return_graduates.append(graduate_dict_final)
            
        return return_graduates
    
    def get_five_random_graduates(db: Session):
        return_graduates = []
        graduates = db.query(Graduates).order_by(func.random()).limit(5).all()

        for graduate in graduates:
            graduate_dict = graduate.__dict__
            graduate_id = graduate_dict["id"]
            graduate_dict_final = User.get_graduate_pictures(db=db, graduate_id=graduate_id)
            return_graduates.append(graduate_dict_final)
            
        return return_graduates
    
    def get_graduates_with_comments_paginated(api_access_code, db: Session, items_per_page: 7, page: 1):
        total_items = db.query(Graduates).count()
        return_graduates = []
        total_pages = (total_items-1)//items_per_page+1
        if page < 1:
            return "Fail-I"
        
        offset = (page-1)*items_per_page

        graduates = db.query(Graduates).order_by(desc(Graduates.created_at)).offset(offset).limit(items_per_page).all()

        for graduate in graduates:
            graduate_dict = graduate.__dict__
            graduate_id = graduate_dict["id"]
            graduate_dict_final = User.get_graduate_pictures(db=db, graduate_id=graduate_id)
            graduate_dict_final["comments"] = User.get_picture_comments_limited(db, graduate_id)
            return_graduates.append(graduate_dict_final)

        page += 1
        fin_resp = {
            'graduates': return_graduates,
            'pagination_url': f'https://knust-alumni-23.vercel.app/user/get-all-graduate-pictures-paginated?page={page}&api_access_code={api_access_code}'
        }
        if page > total_pages:
            fin_resp["pagination_url"] = None
            
        return fin_resp
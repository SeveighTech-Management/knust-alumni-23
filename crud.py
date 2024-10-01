from uuid import UUID, uuid4
from werkzeug.utils import secure_filename
from aws import get_files, send_files
from schema import AddComment
from models import Comments, Graduates
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")


class User:
    @staticmethod
    async def add_graduate(session: Session, graduate):
        try:
            filename = secure_filename(graduate["picture"].filename)
            unique_filename = str(uuid4())
            image_filename = unique_filename + filename[-4:]
            image_binary = await graduate["picture"].read()
            send_files(
                image_binary,
                image_filename,
                graduate["picture"].content_type,
            )
        except Exception as e:
            print(e)
            return "Fail-A"

        try:
            pic = {
                "graduate_name": graduate["graduate_name"],
                "graduate_year": graduate["graduate_year"],
                "graduate_description": graduate["graduate_description"],
                "picture_name": image_filename,
            }
            pic_to_send = Graduates(**pic)
            session.add(pic_to_send)
            session.commit()
            session.refresh(pic_to_send)
        except Exception as e:
            print(e)
            return "Fail-D"

        graduate_id = pic_to_send.id
        picture_details = User.get_graduate_pictures(session, graduate_id)
        picture_details["graduate_year"] = graduate["graduate_year"]
        picture_details["graduate_description"] = graduate["graduate_description"]
        return picture_details

    @staticmethod
    def add_comments(session: Session, comment: AddComment):
        try:
            comment_dict = comment.__dict__
            comment_to_send = Comments(**comment_dict)
            session.add(comment_to_send)
            session.commit()
            session.refresh(comment_to_send)
            return comment_to_send
        except Exception as e:
            print(e)
            return "Fail"

    @staticmethod
    def get_graduate_pictures(session: Session, graduate_id: UUID):
        picture = session.query(Graduates).filter(Graduates.id == graduate_id).first()
        if picture is None:
            return "E"
        picture_dict = picture.__dict__
        details = {
            "id": picture_dict["id"],
            "graduate_name": picture_dict["graduate_name"],
            "graduate_year": picture_dict["graduate_year"],
            "graduate_description": picture_dict["graduate_description"],
            "picture_name": picture_dict["picture_name"],
            "picture_link": "",
        }
        if details["picture_name"] is not None:
            file_name = details["picture_name"]
            details["picture_link"] = get_files(f"{file_name}")
        return details

    @staticmethod
    def get_all_picture_comments(session: Session, graduate_id: UUID):
        graduate = session.query(Graduates).filter(Graduates.id == graduate_id).first()

        graduate_dict = graduate.__dict__
        graduate_id: UUID = graduate_dict["id"]
        graduate_dict_final = User.get_graduate_pictures(
            session=session, graduate_id=graduate_id
        )
        return_comments = []
        comments = (
            session.query(Comments).filter(Comments.graduate_id == graduate_id).all()
        )
        for comment in comments:
            comment_dict = comment.__dict__
            return_comments.append(comment_dict)
        graduate_dict_final["comments"] = return_comments
        return graduate_dict_final

    @staticmethod
    def get_picture_comments_limited(session: Session, graduate_id: UUID):
        return_comments = []
        comments = (
            session.query(Comments)
            .filter(Comments.graduate_id == graduate_id)
            .limit(3)
            .all()
        )
        for comment in comments:
            comment_dict = comment.__dict__
            return_comments.append(comment_dict)
        return return_comments

    @staticmethod
    def check_secret_key(secret_key: str, secret_key_access: str):
        if secret_key != secret_key_access:
            return "Fail"

    @staticmethod
    def get_five_random_graduates(session: Session):
        return_graduates = []
        graduates = session.query(Graduates).order_by(func.random()).limit(5).all()

        for graduate in graduates:
            graduate_dict = graduate.__dict__
            graduate_id = graduate_dict["id"]
            graduate_dict_final = User.get_graduate_pictures(
                session=session, graduate_id=graduate_id
            )
            return_graduates.append(graduate_dict_final)

        return return_graduates

    @staticmethod
    def get_graduates_with_comments_paginated(
        api_access_code, session: Session, items_per_page: int = 7, page: int = 1
    ):
        total_items = session.query(Graduates).count()
        return_graduates = []
        total_pages = (total_items - 1) // items_per_page + 1
        if page < 1:
            return "Fail-I"

        offset = (page - 1) * items_per_page

        graduates = (
            session.query(Graduates)
            .order_by(desc(Graduates.created_at))
            .offset(offset)
            .limit(items_per_page)
            .all()
        )

        for graduate in graduates:
            graduate_dict = graduate.__dict__
            graduate_id = graduate_dict["id"]
            graduate_dict_final = User.get_graduate_pictures(
                session=session, graduate_id=graduate_id
            )
            graduate_dict_final["comments"] = User.get_picture_comments_limited(
                session, graduate_id
            )
            return_graduates.append(graduate_dict_final)

        page += 1
        fin_resp = {
            "graduates": return_graduates,
            "pagination_url": f"https://knust-alumni-23.vercel.app/user/get-all-graduate-pictures-paginated?page={page}&api_access_code={api_access_code}",
        }
        if page > total_pages:
            fin_resp["pagination_url"] = None

        return fin_resp

    @staticmethod
    def get_graduates_with_comments_by_year_paginated(
        api_access_code,
        year: str,
        session: Session,
        items_per_page: int = 7,
        page: int = 1,
    ):
        total_items = (
            session.query(Graduates).filter(Graduates.graduate_year == year).count()
        )
        return_graduates = []
        total_pages = (total_items - 1) // items_per_page + 1
        if page < 1:
            return "Fail-I"

        offset = (page - 1) * items_per_page

        graduates = (
            session.query(Graduates)
            .filter(Graduates.graduate_year == year)
            .order_by(desc(Graduates.created_at))
            .offset(offset)
            .limit(items_per_page)
            .all()
        )

        for graduate in graduates:
            graduate_dict = graduate.__dict__
            graduate_id = graduate_dict["id"]
            graduate_dict_final = User.get_graduate_pictures(
                session=session, graduate_id=graduate_id
            )
            graduate_dict_final["comments"] = User.get_picture_comments_limited(
                session, graduate_id
            )
            return_graduates.append(graduate_dict_final)

        page += 1
        fin_resp = {
            "graduates": return_graduates,
            "pagination_url": f"https://knust-alumni-23.vercel.app/user/filter-graduates-by-year/{year}?page={page}&api_access_code={api_access_code}",
        }
        if page > total_pages:
            fin_resp["pagination_url"] = None

        return fin_resp

    @staticmethod
    def get_graduates_with_comments_by_name_paginated(
        api_access_code,
        name: str,
        session: Session,
        items_per_page: int = 7,
        page: int = 1,
    ):
        total_items = (
            session.query(Graduates)
            .filter(Graduates.graduate_name.ilike(f"%{name}%"))
            .count()
        )
        return_graduates = []
        total_pages = (total_items - 1) // items_per_page + 1
        if page < 1:
            return "Fail-I"

        offset = (page - 1) * items_per_page

        graduates = (
            session.query(Graduates)
            .filter(Graduates.graduate_name.ilike(f"%{name}%"))
            .order_by(desc(Graduates.created_at))
            .offset(offset)
            .limit(items_per_page)
            .all()
        )

        for graduate in graduates:
            graduate_dict = graduate.__dict__
            graduate_id = graduate_dict["id"]
            graduate_dict_final = User.get_graduate_pictures(
                session=session, graduate_id=graduate_id
            )
            graduate_dict_final["comments"] = User.get_picture_comments_limited(
                session, graduate_id
            )
            return_graduates.append(graduate_dict_final)

        page += 1
        fin_resp = {
            "graduates": return_graduates,
            "pagination_url": f"https://knust-alumni-23.vercel.app/user/search-graduates-by-name/{name}?page={page}&api_access_code={api_access_code}",
        }
        if page > total_pages:
            fin_resp["pagination_url"] = None

        return fin_resp

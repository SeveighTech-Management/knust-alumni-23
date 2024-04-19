from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class JobTitles(Base):
    __tablename__ = "job_titles"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    job_name = Column("job_name", String)
    graduate_info = relationship("Graduates", back_populates="job_info")


class Courses(Base):
    __tablename__ = "courses"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    course_name = Column("course_name", String)
    graduate_info = relationship("Graduates", back_populates="course_info")


class Colleges(Base):
    __tablename__ = "colleges"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    colleges_name = Column("college_name", String)
    graduate_info = relationship("Graduates", back_populates="college_info")


class Country(Base):
    __tablename__ = "country"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    country_name = Column("country_name", String)
    graduate_info = relationship("Graduates", back_populates="country_info")


class Gender(Base):
    __tablename__ = "gender"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    gender_name = Column("gender_name", String)
    graduate_info = relationship("Graduates", back_populates="gender_info")


class Graduates(Base):
    __tablename__ = "graduates"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    graduate_name = Column("graduate_name", String(2004))
    graduate_description = Column("graduate_description", String(2004))
    graduate_year = Column("graduate_year", String(2004))
    graduate_reference_number = Column("graduate_reference_number", String(2004))
    picture_name = Column("picture_name", String(2004))
    place_of_work = Column("place_of_work", String(2004))
    password = Column("password", String(2004))
    otp = Column("otp", String(2004))
    email = Column("email", String(2004))
    phone_number = Column("phone_number", String(2004))
    comment = relationship("Comments", back_populates="graduate_info")
    notification_info = relationship("Notifications", back_populates="graduate_info")
    opportunity_info = relationship("Opportunities", back_populates="graduate_info")
    news_update_info = relationship("NewsUpdates", back_populates="graduate_info")
    chat_message_info = relationship("ChatMessages", back_populates="graduate_info")
    job_id = Column("job_id", ForeignKey(JobTitles.id))
    job_info = relationship("JobTitles", back_populates="graduate_info")
    course_id = Column("course_id", ForeignKey(Courses.id))
    course_info = relationship("Courses", back_populates="graduate_info")
    college_id = Column("college_id", ForeignKey(Colleges.id))
    college_info = relationship("Colleges", back_populates="graduate_info")
    country_id = Column("country_id", ForeignKey(Country.id))
    country_info = relationship("Country", back_populates="graduate_info")
    gender_id = Column("gender_id", ForeignKey(Gender.id))
    gender_info = relationship("Gender", back_populates="graduate_info")


class Comments(Base):
    __tablename__ = "comments"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    comment = Column("comment", String(2004))
    name_of_commenter = Column("name_of_commenter", String(2004))
    graduate_id = Column(UUID(as_uuid=True), ForeignKey(Graduates.id))
    graduate_info = relationship("Graduates", back_populates="comment")


class Notifications(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    title = Column("title", String(2004))
    details = Column("details", String(2004))
    graduate_id = Column(UUID(as_uuid=True), ForeignKey(Graduates.id))
    graduate_info = relationship("Graduates", back_populates="notification_info")


class OpportunityTypes(Base):
    __tablename__ = "opportunity_type"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    type_name = Column("type_name", String(2004))
    opportunity_info = relationship("Opportunities", back_populates="opportunity_type_info")


class Opportunities(Base):
    __tablename__ = "opportunities"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    title = Column("title", String(2004))
    description = Column("description", String(2004))
    media = Column("media", String(2004))
    opportunity_type_id = Column(UUID(as_uuid=True), ForeignKey(OpportunityTypes.id))
    opportunity_type_info = relationship("OpportunityTypes", back_populates="opportunity_info")
    graduate_id = Column("poster_id", ForeignKey(Graduates.id))
    graduate_info = relationship("Graduates", back_populates="opportunity_info")


class NewsUpdates(Base):
    __tablename__ = "news_updates"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    title = Column("title", String(2004))
    description = Column("description", String(2004))
    media = Column("media", String(2004))
    graduate_id = Column("poster_id", ForeignKey(Graduates.id))
    graduate_info = relationship("Graduates", back_populates="news_update_info")


class ChatRooms(Base):
    __tablename__ = "chat_rooms"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    chat_name = Column("chat_name", String(2004))
    chat_description = Column("chat_description", String(2004))
    chat_picture = Column("chat_picture", String(2004))
    chat_message_info = relationship("ChatMessages", back_populates="chat_room_info")


class ChatMessages(Base):
    __tablename__ = "chat_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    chat_id = Column("chat_id", ForeignKey(ChatRooms.id))
    chat_room_info = relationship("ChatRooms", back_populates="chat_message_info")
    graduate_id = Column("graduate_id", ForeignKey(Graduates.id))
    graduate_info = relationship("Graduates", back_populates="chat_message_info")

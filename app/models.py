from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    lesson_type = Column(String, nullable=False)
    is_downloaded = Column(Integer, default=0)  # 0 = preloaded, 1 = downloaded


class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)
    score = Column(Integer, nullable=False)


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    class_level = Column(String, nullable=False)  # e.g., "JSS1", "SS2"
    subject_name = Column(String, nullable=False)  # e.g., "Math"
    is_preinstalled = Column(Boolean, default=False)
    s3_key = Column(String, nullable=True)  # S3 path for downloadable content


class DownloadedResource(Base):
    __tablename__ = "downloaded_resources"
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, nullable=False)
    filepath = Column(String, nullable=False)  # Local path on device
    is_downloaded = Column(Boolean, default=False)

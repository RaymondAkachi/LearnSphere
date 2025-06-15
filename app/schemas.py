from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    grade: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class LessonBase(BaseModel):
    title: str
    subject: str
    filepath: str
    lesson_type: str
    is_downloaded: Optional[int] = 0


class LessonCreate(LessonBase):
    pass


class Lesson(LessonBase):
    id: int

    class Config:
        orm_mode = True


class SubjectBase(BaseModel):
    class_level: str
    subject_name: str
    is_preinstalled: bool
    s3_key: Optional[str] = None


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int

    class Config:
        orm_mode = True


class DownloadedResourceBase(BaseModel):
    subject_id: int
    filepath: str
    is_downloaded: bool


class DownloadedResourceCreate(DownloadedResourceBase):
    pass


class DownloadedResource(DownloadedResourceBase):
    id: int

    class Config:
        orm_mode = True

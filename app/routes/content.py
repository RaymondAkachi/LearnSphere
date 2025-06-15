from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base
from app.models import Lesson
from app.schemas import Lesson, LessonCreate, Subject, SubjectCreate, DownloadedResource
from app.utils.file_handler import save_content_pack
from app.utils.s3_handler import download_from_s3
import os

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Preload initial subjects


def preload_subjects(db: Session):
    if db.query(Subject).count() == 0:
        preinstalled = [
            SubjectCreate(class_level="JSS1", subject_name="Math",
                          is_preinstalled=True),
            SubjectCreate(class_level="JSS2", subject_name="Math",
                          is_preinstalled=True),
            SubjectCreate(class_level="JSS3", subject_name="Math",
                          is_preinstalled=True),
            SubjectCreate(class_level="SS1", subject_name="Math",
                          is_preinstalled=False, s3_key="ss1_math.zip"),
        ]
        for subject in preinstalled:
            db_subject = Subject(**subject.dict())
            db.add(db_subject)
        db.commit()


@router.get("/subjects", response_model=list[Subject])
def get_subjects(db: Session = Depends(get_db)):
    preload_subjects(db)
    return db.query(Subject).all()


@router.post("/download/{subject_id}")
def download_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject or subject.is_preinstalled:
        raise HTTPException(
            status_code=400, detail="Subject not downloadable or already preinstalled")

    s3_key = subject.s3_key
    local_zip = f"downloads/{s3_key}"
    os.makedirs("downloads", exist_ok=True)

    download_from_s3(s3_key, local_zip)
    save_content_pack(
        local_zip, f"content_packs/{subject.class_level}_{subject.subject_name}")

    resource = DownloadedResource(
        subject_id=subject_id, filepath=local_zip, is_downloaded=True)
    db.add(resource)
    db.commit()

    return {"message": f"Downloaded {subject.class_level} {subject.subject_name}", "filepath": local_zip}


@router.post("/save-lesson", response_model=Lesson)
def save_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

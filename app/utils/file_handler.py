import zipfile
import os
import json
import shutil


def save_content_pack(zip_path, dest_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    os.remove(zip_path)


def load_content(subject_folder: str):
    with open(os.path.join(subject_folder, 'lessons.json')) as f:
        lessons = json.load(f)
    with open(os.path.join(subject_folder, 'quizzes.json')) as f:
        quizzes = json.load(f)
    with open(os.path.join(subject_folder, 'explanations.json')) as f:
        explanations = json.load(f)
    return lessons, quizzes, explanations

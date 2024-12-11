import os
from werkzeug.utils import secure_filename
from src.config import Config

def handle_file_upload(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        file.save(filepath)
        return '', 204
    else:
        file.save(filepath)
        return '', 201

def list_files_in_directory():
    try:
        return os.listdir(Config.UPLOAD_FOLDER)
    except FileNotFoundError:
        return []

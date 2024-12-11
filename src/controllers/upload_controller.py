# src/controllers/upload_controller.py
from flask import request, jsonify
import re

def upload_file():
    from src.services.file_service import handle_file_upload  # Importação local

    file = request.files.get('file')
    breakpoint()
    if not file:
        return jsonify({"error": "No file part in the request"}), 400

    filename = file.filename
    if not filename or not re.match(r'^[A-Za-z0-9_.-]+$', filename):
        return jsonify({"error": "Invalid file name"}), 400

    result, status_code = handle_file_upload(file)
    return result, status_code

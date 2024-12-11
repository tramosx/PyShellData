import os

from flask import request, jsonify
from src.services.bash_service import execute_bash_script
from src.utils.utils import parse_line_to_json
from src.config import Config

def get_size_user(mode):
    filename = request.args.get('file')

    if not filename:
        return jsonify({"error": "File name is required"}), 400
    
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404


    result, error = execute_bash_script(filepath, mode)
    if error:
        return jsonify({"error": error}), 500

    user_data = parse_line_to_json(result)

    return jsonify(user_data), 200

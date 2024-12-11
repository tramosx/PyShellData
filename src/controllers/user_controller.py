import os

from flask import request, jsonify
from src.config import Config


def get_user():
    from src.services.user_service import get_users_sorted

    filename = request.args.get('file')
    desc = request.args.get('desc', 'false').lower() == 'true'
    filter_username = request.args.get('username')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if not filename:
        return jsonify({"error": "File name is required"}), 400
    
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404


    users = get_users_sorted(filepath, filter_username, desc)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = users[start:end]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(users),
        "total_pages": (len(users) // per_page) + (1 if len(users) % per_page != 0 else 0),
        "users": paginated_users
    })

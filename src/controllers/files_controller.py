from flask import request, jsonify
from src.services.file_service import list_files_in_directory


def list_files():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    files = list_files_in_directory()
    start = (page - 1) * per_page
    end = start + per_page
    paginated_files = files[start:end]

    return jsonify({
        "files": paginated_files,
        "page": page,
        "per_page": per_page,
        "total_files": len(files)
    })

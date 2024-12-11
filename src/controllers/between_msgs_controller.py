from flask import request, jsonify

from src.services.bash_service import execute_bash_script_between_msgs
from src.utils.utils import parse_line_to_json, extract_username


def between_msgs():
    filename = request.args.get('file')
    qtd_min = request.args.get('qtd_min')
    qtd_max = request.args.get('qtd_max')
    filter_username = request.args.get('username')


    if not filename or not qtd_min or not qtd_max:
        return jsonify({"error": "File name and message quantity are required"}), 400

    output, error = execute_bash_script_between_msgs(filename, qtd_min, qtd_max)

    if error:
        return jsonify({"error": error}), 500


    users = []
    for line in output.strip().split('\n'):
        user_data = parse_line_to_json(line)

        if filter_username:
            username_from_email = extract_username(user_data['username'])
            if filter_username != username_from_email:
                continue

        users.append(user_data)


    return jsonify({"users": users}), 200
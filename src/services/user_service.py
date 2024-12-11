from src.services.bash_service import execute_bash_script_sorted
from src.utils.utils import parse_line_to_json, extract_username


def get_users_sorted(filename, filter_username, desc):
    output, error = execute_bash_script_sorted(filename, desc)
    if error:
        return []

    users = []
    for line in output.strip().split('\n'):
        user_data = parse_line_to_json(line)
        if filter_username:
            username_from_email = extract_username(user_data['username'])
            if filter_username != username_from_email:
                continue
        users.append(user_data)

    return users
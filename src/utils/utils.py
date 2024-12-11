

def parse_line_to_json(line):
    parts = line.split()
    return {
        "username": parts[0],
        "folder": parts[1],
        "numberMessages": int(parts[2]),
        "size": parts[4]
    }


def extract_username(email):
    return email.split('@')[0]
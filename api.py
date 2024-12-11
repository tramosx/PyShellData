from flask import Flask, request, jsonify, abort
import os
import re
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/teste-api'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garantir que o diretório de upload exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Expressão regular para validar o nome do arquivo
VALID_FILENAME_REGEX = re.compile(r'^[A-Za-z0-9_.-]+$')

# 1 - Upload de arquivo
@app.route('/upload', methods=['PUT'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not VALID_FILENAME_REGEX.match(file.filename):
        return jsonify({"error": "Invalid file name"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        file.save(filepath)
        return '', 204  # Arquivo substituído
    else:
        file.save(filepath)
        return '', 201  # Arquivo novo criado

# 2 - Listagem de arquivos com paginação (opcional)
@app.route('/files', methods=['GET'])
def list_files():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
    except FileNotFoundError:
        return jsonify({"error": "Upload folder not found"}), 500

    start = (page - 1) * per_page
    end = start + per_page
    paginated_files = files[start:end]

    return jsonify({"files": paginated_files, "page": page, "per_page": per_page, "total_files": len(files)}), 200

# 3 - Obter usuário com maior ou menor size
@app.route('/size/<string:mode>', methods=['GET'])
def get_size_user(mode):
    filename = request.args.get('file')

    if not filename:
        return jsonify({"error": "File name is required"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    if mode not in ['max', 'min']:
        return jsonify({"error": "Invalid mode. Use 'max' or 'min'"}), 400

    mode = f"-{mode}"

    # Executar o script bash para obter maior ou menor size
    script = './max-min-size.sh'
    try:
        result = subprocess.run([script, filepath, mode], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output:
            return jsonify({"error": "No data found in the file"}), 404

        # Converter a saída para JSON
        user_data = output.split()
        response = {
            "username": user_data[0],
            "folder": user_data[1],
            "numberMessages": int(user_data[2]),
            "size": int(user_data[4])
        }
        return jsonify(response), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Error processing file", "details": e.stderr.strip()}), 500


# Função para executar o script bash e retornar a saída
def execute_bash_script(input_file, desc_option=False):
    try:
        # Definir o comando para execução
        cmd = ['./order-by-username.sh', input_file, '-desc' if desc_option else '']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        breakpoint()
        if result.returncode != 0:
            return None, result.stderr
        
        return result.stdout, None
    except Exception as e:
        return None, str(e)
    



def execute_bash_script2(input_file, qtd_min, qtd_max):
    try:
        # Definir o comando para execução
        cmd = ['./between-msgs.sh', input_file, qtd_min, qtd_max]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            return None, result.stderr
        
        return result.stdout, None
    except Exception as e:
        return None, str(e)



# Função para converter a linha do arquivo em JSON
def parse_line_to_json(line):
    parts = line.split()
    return {
        "username": parts[0],
        "folder": parts[1],
        "numberMessages": int(parts[2]),
        "size": parts[4]
    }



# Função para extrair o nome de usuário (parte antes do '@')
def extract_username(email):
    return email.split('@')[0]



@app.route('/users', methods=['GET'])
def get_user():
    filename = request.args.get('file')
    desc = request.args.get('desc', 'false').lower() == 'true'
    filter_username = request.args.get('username')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if not filename:
        return jsonify({"error": "File name is required"}), 400

    output, error = execute_bash_script(filename, desc)

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





@app.route('/between-msgs', methods=['GET'])
def between_msgs():
    filename = request.args.get('file')
    qtd_min = request.args.get('qtd_min')
    qtd_max = request.args.get('qtd_max')
    filter_username = request.args.get('username')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if not filename:
        return jsonify({"error": "File name is required"}), 400

    breakpoint()
    output, error = execute_bash_script2(filename, qtd_min, qtd_max)

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






if __name__ == '__main__':
    app.run(debug=True)

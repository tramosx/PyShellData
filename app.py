from flask import Flask
import os

from src.controllers.upload_controller import upload_file
from src.controllers.size_controller import get_size_user
from src.controllers.files_controller import list_files
from src.controllers.user_controller import get_user
from src.controllers.between_msgs_controller import between_msgs

def create_app():
    app = Flask(__name__)

    # Configuração
    app.config.from_object('src.config.Config')

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Registra as rotas
    app.add_url_rule('/upload', 'upload', upload_file, methods=['PUT'])
    app.add_url_rule('/files', 'list_files', list_files, methods=['GET'])
    app.add_url_rule('/size/<string:mode>', 'get_size_user', get_size_user, methods=['GET'])
    app.add_url_rule('/users', 'get_user', get_user, methods=['GET'])
    app.add_url_rule('/between-msgs', 'between_msgs', between_msgs, methods=['GET'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000)


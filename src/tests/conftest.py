import pytest
from app import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    """Configura a aplicação Flask para testes."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app):
    """Cria um cliente de teste."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Cria um runner de comandos para a aplicação."""
    return app.test_cli_runner()


@pytest.fixture
def mock_between_msgs():
    with patch('src.controllers.between_msgs_controller.execute_bash_script_between_msgs', 
               return_value=("user1@teste.com inbox 2 size 002142222\nuser2@teste.com inbox 2 size 001032646", None)) as mock_execute, \
         patch('src.utils.utils.parse_line_to_json', 
               side_effect=lambda line: {
                   "username": line.split()[0],
                   "message_count": int(line.split()[1])
               }) as mock_parse, \
         patch('src.utils.utils.extract_username', 
               side_effect=lambda email: email.split('@')[0]) as mock_extract:

        yield mock_execute, mock_parse, mock_extract


@pytest.fixture
def mock_parse_line_to_json(mocker):
    """Mocka a função parse_line_to_json."""
    return mocker.patch('src.utils.utils.parse_line_to_json')

@pytest.fixture
def mock_extract_username(mocker):
    """Mocka a função extract_username."""
    return mocker.patch('src.utils.utils.extract_username')

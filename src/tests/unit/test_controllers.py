import pytest
from unittest.mock import patch


def test_between_msgs_success(client, mock_between_msgs):
    # Faz a requisição simulada
    response = client.get(
        '/between-msgs',
        query_string={
            'file': 'test_file.txt',
            'qtd_min': '3',
            'qtd_max': '10',
            'username': 'user1'
        }
    )

    # Verifica o resultado
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['users']) == 1
    assert data['users'][0]['username'] == 'user1@teste.com'
    assert data['users'][0]['numberMessages'] == 2


def test_between_msgs_missing_params(client):
    response = client.get('/between-msgs')
    assert response.status_code == 400
    assert response.get_json() == {"error": "File name and message quantity are required"}


def test_list_files(client):
    mock_files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]

    # Mocka a função list_files_in_directory
    with patch('src.controllers.files_controller.list_files_in_directory', return_value=mock_files):
        response = client.get('/files', query_string={"page": 1, "per_page": 2})

    # Verifica a resposta da API
    assert response.status_code == 200
    data = response.get_json()

    assert data["files"] == ["file1.txt", "file2.txt"]
    assert data["page"] == 1
    assert data["per_page"] == 2
    assert data["total_files"] == 4
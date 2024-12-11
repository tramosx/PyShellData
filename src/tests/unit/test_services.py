import subprocess
from unittest import mock
import pytest
from src.services.bash_service import execute_bash_script


def test_execute_bash_script_success():
    input_file = 'testfile.txt'
    mode = 'max'
    expected_output = "username testuser size 1234"
    
    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = expected_output
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        
        output, error = execute_bash_script(input_file, mode)
        
        assert output == expected_output
        assert error is None


def test_execute_bash_script_no_output():
    input_file = 'testfile.txt'
    mode = 'max'
    
    with mock.patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        
        output, error = execute_bash_script(input_file, mode)
        
        assert output == {"error": "No data found in the file"}
        assert error is None

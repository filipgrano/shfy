import subprocess
import sys
from unittest.mock import Mock

import pytest

from shfy.shfy import explain_command, generate_command, main


@pytest.fixture
def mock_openai_create(mocker):
    mock = mocker.patch("shfy.shfy.client.chat.completions.create")
    yield mock


def test_generate_command(mock_openai_create):  # pylint: disable=redefined-outer-name
    mock_openai_create.return_value = Mock(choices=[Mock(message=Mock(content="suggested_command"))])

    response = generate_command("prompt")
    assert response.choices[0].message.content == "suggested_command"
    mock_openai_create.assert_called_once()


def test_explain_command(mock_openai_create):  # pylint: disable=redefined-outer-name
    mock_openai_create.return_value = Mock(choices=[Mock(message=Mock(content="explanation"))])

    response = explain_command("suggestion", "prompt")
    assert response.choices[0].message.content == "explanation"
    mock_openai_create.assert_called_once()


def test_execute_command_stdout_and_stderr():
    # Prepare the command to run the execute_command function in a separate Python process
    python_code = """
import sys
from shfy.shfy import execute_command

command = "echo 'Hello, World!' && echo 'Error: Test' >&2"
execute_command(command)
    """

    # Run the Python code and capture stdout and stderr
    result = subprocess.run(
        ["python", "-c", python_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
    )

    # Check the content of the captured standard output and standard error
    assert result.stdout.strip() == "Hello, World!"
    assert result.stderr.strip() == "Error: Test"


def test_main_explain_only(mocker):
    generate_command_mock = mocker.patch(
        "shfy.shfy.generate_command", return_value=Mock(choices=[Mock(message=Mock(content="suggested_command"))])
    )
    explain_command_mock = mocker.patch(
        "shfy.shfy.explain_command", return_value=Mock(choices=[Mock(message=Mock(content="explanation"))])
    )
    execute_command_mock = mocker.patch("shfy.shfy.execute_command")
    mocker.patch(
        "builtins.input", side_effect=["e", "n"]
    )  # User chooses to explain the command first, then chooses not to execute

    mocker.patch.object(sys, "argv", ["script_name", "prompt"])

    main()

    generate_command_mock.assert_called_with("prompt")
    explain_command_mock.assert_called_once_with("suggested_command", "prompt")
    execute_command_mock.assert_not_called()


def test_main_execute_after_explain(mocker):
    generate_command_mock = mocker.patch(
        "shfy.shfy.generate_command", return_value=Mock(choices=[Mock(message=Mock(content="suggested_command"))])
    )
    explain_command_mock = mocker.patch(
        "shfy.shfy.explain_command", return_value=Mock(choices=[Mock(message=Mock(content="explanation"))])
    )
    execute_command_mock = mocker.patch("shfy.shfy.execute_command")
    mocker.patch(
        "builtins.input", side_effect=["e", "y"]
    )  # User chooses to explain the command first, then chooses to execute

    mocker.patch.object(sys, "argv", ["script_name", "prompt"])

    main()

    generate_command_mock.assert_called_with("prompt")
    explain_command_mock.assert_called_once_with("suggested_command", "prompt")
    execute_command_mock.assert_called_once_with("suggested_command")


if __name__ == "__main__":
    pytest.main()

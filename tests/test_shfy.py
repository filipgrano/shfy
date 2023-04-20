import subprocess
import sys

from shfy.shfy import explain_command, generate_command, main


def test_generate_command(mocker):
    mocker.patch(
        "openai.ChatCompletion.create",
        return_value=mocker.Mock(choices=[mocker.Mock(message=mocker.Mock(content="suggested_command"))]),
    )

    response = generate_command("prompt")
    assert response.choices[0].message.content == "suggested_command"


def test_explain_command(mocker):
    mocker.patch(
        "openai.ChatCompletion.create",
        return_value=mocker.Mock(choices=[mocker.Mock(message=mocker.Mock(content="explanation"))]),
    )

    response = explain_command("suggestion", "prompt")
    assert response.choices[0].message.content == "explanation"


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


def test_main(mocker):
    generate_command_mock = mocker.patch("shfy.shfy.generate_command")
    # explain_command_mock =
    mocker.patch("shfy.shfy.explain_command")
    execute_command_mock = mocker.patch("shfy.shfy.execute_command")
    mocker.patch("builtins.input", side_effect=["n"])  # User chooses not to execute the command

    mocker.patch.object(sys, "argv", ["script_name", "prompt"])

    main()

    generate_command_mock.assert_called_with("prompt")
    execute_command_mock.assert_not_called()

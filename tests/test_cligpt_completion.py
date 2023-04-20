import sys
from unittest.mock import MagicMock

import pytest

from oai_tools.cligpt_completion import complete as completion_complete
from oai_tools.cligpt_completion import explain as completion_explain


@pytest.fixture
def mock_generate_command(mocker):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "suggested command 123"
    return mocker.patch("oai_tools.cligpt_completion.generate_command", return_value=mock_response)


def test_completion_complete(mocker, mock_generate_command, capfd):  # pylint: disable=W0621
    mocker.patch.object(sys, "argv", ["completion_script_name", "prompt"])

    completion_complete()

    captured = capfd.readouterr()
    output = captured.out.strip()

    assert output == "suggested command 123"
    mock_generate_command.assert_called_once_with("prompt")


@pytest.fixture
def mock_explain_command(mocker):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "explanation of the command 123"
    return mocker.patch("oai_tools.cligpt_completion.explain_command", return_value=mock_response)


def test_completion_explain(mocker, mock_explain_command, capfd):  # pylint: disable=W0621
    mocker.patch.object(sys, "argv", ["explanation_script_name", "prompt"])

    completion_explain()

    captured = capfd.readouterr()
    output = captured.out.strip()

    assert output == "explanation of the command 123"
    mock_explain_command.assert_called_once_with("prompt")

import sys
from unittest.mock import MagicMock

import pytest

from oai_tools.cligpt_completion import main as completion_main


@pytest.fixture
def mock_generate_command(mocker):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "suggested command 123"
    return mocker.patch("oai_tools.cligpt_completion.generate_command", return_value=mock_response)


def test_completion_main(mocker, mock_generate_command, capfd):  # pylint: disable=W0621
    mocker.patch.object(sys, "argv", ["completion_script_name", "prompt"])

    completion_main()

    captured = capfd.readouterr()
    output = captured.out.strip()

    assert output == "suggested command 123"
    mock_generate_command.assert_called_once_with("prompt")

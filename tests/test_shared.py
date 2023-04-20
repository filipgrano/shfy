import pytest

from shfy import get_api_key, read_config


def test_read_config_existing_file(mocker):
    file_content = "key: value\nkey2: value2\n"

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=file_content))

    result = read_config()
    assert result == {"key": "value", "key2": "value2"}


def test_read_config_non_existing_file(mocker):
    mocker.patch("os.path.exists", return_value=False)

    result = read_config()
    assert result == {}


def test_get_api_key_from_env_var(mocker):
    mocker.patch("os.environ.get", return_value="test_api_key")

    api_key = get_api_key()
    assert api_key == "test_api_key"


def test_get_api_key_from_file(mocker):
    mocker.patch("os.environ.get", return_value=None)
    file_content = "test_api_key_from_file\n"

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=file_content))

    api_key = get_api_key()
    assert api_key == "test_api_key_from_file"


def test_get_api_key_not_found(mocker):
    mocker.patch("os.environ.get", return_value=None)
    mocker.patch("os.path.exists", return_value=False)

    with pytest.raises(ValueError, match="API key not found in environment variable or config file"):
        get_api_key()

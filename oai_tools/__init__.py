import os
import yaml


def read_config() -> dict:
    config_file = os.path.expanduser("~/.config/oai_tools/config.yaml")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return yaml.safe_load(f)
    return {}


def get_api_key() -> str:
    """Get the API key from an environment variable or a file."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    config_file = os.path.expanduser("~/.config/oai_tools/api_key")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return f.read().strip()

    raise ValueError("API key not found in environment variable or config file")

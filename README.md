# OAI Tools

This repository contains a collection of useful tools built on top of OpenAI's API. These tools can help automate various tasks and provide assistance through natural language processing.

## Installation or Upgrade
`pip install --upgrade oai-tools`

## Tools

1. **cligpt**: A command-line helper that takes a user prompt and returns shell commands, along with explanations of what they do. It also supports command completions for various shells. See [cligpt.md](doc/cligpt.md) for more details.

## Configuration
Configuration file is read from `~/.config/oai_tools/config.yaml` file. See the [config-example.yaml](doc/config-example.yaml) file for more details.

### API Key
OpenAI's API key is required. 
The key is read from the `OPENAI_API_KEY` environment variable. If this variable is not set, the API key is read from the `~/.config/oai_tools/api_key` file.

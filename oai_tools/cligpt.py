import logging
import os
import platform
import sys

import openai

from oai_tools import get_api_key, read_config

openai.api_key = get_api_key()

config = read_config()
cligpt_config = config.get("cligpt", {})

LOG_LEVEL = cligpt_config.get("loglevel", "INFO")
logging.basicConfig(level=logging.getLevelName(LOG_LEVEL))

MODEL = cligpt_config.get("model", "gpt-3.5-turbo")
AUTO_EXPLAIN = cligpt_config.get("auto_explain", False)
MAX_TOKENS_COMMAND = cligpt_config.get("max_tokens", {}).get("command", 100)
MAX_TOKENS_EXPLANATION = cligpt_config.get("max_tokens", {}).get("explanation", 100)
TEMPERATURE_COMMAND = cligpt_config.get("temperature", {}).get("command", 0.9)
TEMPERATURE_EXPLANATION = cligpt_config.get("temperature", {}).get("explanation", 0.9)


def get_shell() -> str:
    """Get the default shell for the current platform."""
    system = platform.system()
    if system == "Windows":
        return os.environ.get("COMSPEC", "cmd.exe").strip()
    if system in ["Linux", "Darwin"]:
        return os.environ.get("SHELL", "/bin/bash").strip()

    raise ValueError(f"Unsupported platform: {system}")


def generate_command(prompt: str) -> openai.ChatCompletion:
    """Generate a shell command using GPT-3.5 based on the given prompt."""
    query = f"""Write a shell command that works in the following shell: {get_shell()}

        The command must accomplish this task:

        {prompt}

        Return ONLY the command, no other explanation, words, code highlighting, or text."""

    logging.debug("Generating command for prompt: %s", prompt)

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": query}],
        max_tokens=MAX_TOKENS_COMMAND,
        temperature=TEMPERATURE_COMMAND,
        n=1,
    )
    return response


def explain_command(suggestion: str, prompt: str) -> openai.ChatCompletion:
    """Generate an explanation of a suggested command using GPT-3.5."""
    query = f"Explain in brief how the command '{suggestion}' works, what it does, and if it's safe to use (why not if not). Also state if it fulfills the requested task '{prompt}' or not. Return the explanation and task fulfillment status in a single line. No other words, code highlighting, or text. Don't repeat the command or the task."

    logging.debug("Explaining command: %s", suggestion)

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": query}],
        max_tokens=MAX_TOKENS_EXPLANATION,
        temperature=TEMPERATURE_EXPLANATION,
        n=1,
    )
    return response


def execute_command(command: str) -> None:
    """Execute a shell command and print its output and errors as they are produced."""
    shell = get_shell()
    logging.debug("Executing shell command in shell %s: %s", shell, command)

    command = command.replace('"', r"\"")
    command = f'{shell} -c "{command}" '
    return_code = os.system(command)

    logging.debug("Shell command results -- return code: %s", return_code)


def main():
    try:
        prompt = " ".join(sys.argv[1:])
        logging.debug("Prompt: %s", prompt)

        command_query_response = generate_command(prompt)
        suggestion = command_query_response.choices[0].message.content
        print(f"Suggestion: {suggestion}")

        if AUTO_EXPLAIN:
            explanation_query_response = explain_command(suggestion, prompt)
            explanation = explanation_query_response.choices[0].message.content
            print(f"Explanation: {explanation}")
            confirmation = input("Execute suggested command? (Y/N): ").lower()
        else:
            confirmation = input("Execute suggested command? (Y/N) | Explain command? (E): ").lower()

        while True:
            if confirmation == "e" and not AUTO_EXPLAIN:
                explanation_query_response = explain_command(suggestion, prompt)
                explanation = explanation_query_response.choices[0].message.content
                print(f"Explanation: {explanation}")
                confirmation = input("Execute suggested command? (Y/N): ").lower()
            elif confirmation == "y":
                execute_command(suggestion)
                break
            elif confirmation == "n":
                print("Phew, good that I asked...")
                break
            else:
                print("Invalid input. Please enter Y, N, or E.")
                confirmation = input("Execute suggested command? (Y/N) | Explain command? (E): ").lower()
    except KeyboardInterrupt:
        print("\nAborted by user.")


if __name__ == "__main__":
    main()

import logging
import os
import platform
import sys

from openai import OpenAI
from openai.types.chat import ChatCompletion

from shfy import get_api_key, read_config

client = OpenAI(api_key=get_api_key())

config = read_config()

LOG_LEVEL = config.get("loglevel", "WARNING")
logging.basicConfig(level=logging.getLevelName(LOG_LEVEL))

MODEL = config.get("model", "gpt-3.5-turbo")
AUTO_EXPLAIN = config.get("auto_explain", False)
MAX_TOKENS_COMMAND = config.get("max_tokens", {}).get("command", 100)
MAX_TOKENS_EXPLANATION = config.get("max_tokens", {}).get("explanation", 100)
TEMPERATURE_COMMAND = config.get("temperature", {}).get("command", 0.1)
TEMPERATURE_EXPLANATION = config.get("temperature", {}).get("explanation", 0.1)


def get_shell() -> str:
    """Get the default shell for the current platform."""
    system = platform.system()
    if system == "Windows":
        shell = os.environ.get("COMSPEC", "cmd.exe")
    else:
        shell = os.environ.get("SHELL", "/bin/bash")

    if shell is None:
        raise ValueError(f"Unsupported platform or missing shell environment variable: {system}")

    return shell.strip()


def generate_command(prompt: str) -> ChatCompletion:
    """Generate a shell command based on the given prompt."""
    system_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    shell_name = os.path.basename(get_shell())

    query = f"""
        Write a shell command that works on the {system_info} platform in the {shell_name} shell.

        The command must accomplish this task:

        {prompt}

        Return ONLY the command, no other explanation, words, code highlighting, or text.
    """

    logging.debug("Generating command for prompt: %s", prompt)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": query}],
        max_tokens=MAX_TOKENS_COMMAND,
        temperature=TEMPERATURE_COMMAND,
        n=1,
    )
    return response


def explain_command(suggestion: str, prompt: str = "") -> ChatCompletion:
    """Generate an explanation of a suggested command."""
    system_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    shell_name = os.path.basename(get_shell())

    if prompt == "":
        query = f"""
            Explain in brief how the command '{suggestion}' works on the {system_info} platform in the {shell_name} shell, what it does, and if it's safe to use (why not if not). Return the explanation in a single line. No other words, code highlighting, or text. Don't repeat the command or the task.
        """
    else:
        query = f"""
            Explain in brief how the command '{suggestion}' works on the {system_info} platform in the {shell_name} shell, what it does, and if it's safe to use (why not if not). Also state if it fulfills the requested task '{prompt}' or not. Return the explanation and task fulfillment status in a single line. No other words, code highlighting, or text. Don't repeat the command or the task.
        """

    logging.debug("Explaining command: %s", suggestion)

    response = client.chat.completions.create(
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

    if platform.system() == "Windows":
        if "powershell" in shell.lower():
            command = f'powershell.exe -Command "& {{ {command} }}"'
        else:
            command = f'cmd.exe /C "{command}"'
    else:
        command = command.replace('"', r"\"")
        command = command.replace("$", r"\$")
        command = f'{shell} -c "{command}"'

    return_code = os.system(command)

    logging.debug("Shell command results -- return code: %s", return_code)


def main() -> None:
    try:
        prompt = " ".join(sys.argv[1:])
        logging.debug("Prompt: %s", prompt)

        command_query_response = generate_command(prompt)
        suggestion = command_query_response.choices[0].message.content

        if suggestion is None:
            raise ValueError("No suggestion returned from OpenAI")

        print(f"Suggestion: {suggestion}")

        if AUTO_EXPLAIN:
            explanation_query_response = explain_command(suggestion, prompt)
            explanation = explanation_query_response.choices[0].message.content

            if explanation is None:
                raise ValueError("No explanation returned from OpenAI")

            print(f"Explanation: {explanation}")
            confirmation = input("Execute suggested command? (Y/N): ").lower()
        else:
            confirmation = input("Execute suggested command? (Y/N) | Explain command? (E): ").lower()

        while True:
            if confirmation == "e" and not AUTO_EXPLAIN:
                explanation_query_response = explain_command(suggestion, prompt)
                explanation = explanation_query_response.choices[0].message.content

                if explanation is None:
                    raise ValueError("No explanation returned from OpenAI")

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
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

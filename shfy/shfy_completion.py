import sys

from shfy.shfy import explain_command, generate_command


def complete() -> None:
    try:
        prompt = " ".join(sys.argv[1:])
        completion_response = generate_command(prompt)
        completion = completion_response.choices[0].message.content
        if completion is None:
            raise ValueError("No completion returned from OpenAI")
        print(completion.strip())
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


def explain() -> None:
    try:
        prompt = " ".join(sys.argv[1:])
        explanation_response = explain_command(prompt)
        explanation = explanation_response.choices[0].message.content
        if explanation is None:
            raise ValueError("No explanation returned from OpenAI")
        print(explanation.strip())
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

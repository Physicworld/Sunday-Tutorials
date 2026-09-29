import os
import sys
from pprint import pprint

from LLMAPI import LMStudioAPIWrapper, LMStudioError

MODEL = os.environ.get(
    "LMSTUDIO_MODEL",
    "lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
)

def main():
    # Example usage
    api_wrapper = LMStudioAPIWrapper()

    # Example for get_models
    models = api_wrapper.get_models()
    print("Models:")
    pprint(models)
    print()

    # Example for post_chat_completions
    chat_data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "Hola!"}]
    }
    chat_response = api_wrapper.post_chat_completions(chat_data)

    print("Chat Completions Response:")
    pprint(chat_response)
    print()

    # Example for post_completions
    completion_data = {
        "model": MODEL,
        "prompt": "Habia una vez..."
    }
    completion_response = api_wrapper.post_completions(completion_data)
    print("Completions Response:")
    pprint(completion_response)


if __name__ == "__main__":
    try:
        main()
    except LMStudioError as exc:
        sys.exit(f"Error: {exc}")

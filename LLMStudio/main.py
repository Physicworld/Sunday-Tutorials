from LLMAPI import LMStudioAPIWrapper
from pprint import pprint

# Example usage
api_wrapper = LMStudioAPIWrapper()

# Example for get_models
models = api_wrapper.get_models()
print("Models:")
pprint(models)
print()

# Example for post_chat_completions
chat_data = {
    "model": "lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
    "messages": [{"role": "user", "content": "Hola!"}]
}
chat_response = api_wrapper.post_chat_completions(chat_data)

print("Chat Completions Response:")
pprint(chat_response)
print()

# Example for post_completions
completion_data = {
    "model": "lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
    "prompt": "Habia una vez..."
}
completion_response = api_wrapper.post_completions(completion_data)
print("Completions Response:")
pprint(completion_response)

# Large language model used to comunicate with the user and the system

import requests
import json
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b"

def ask_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()
    data = response.json()

    return data["response"]


if __name__ == "__main__":
    text = """
        You are the language model for a personal AI assistant.

        Always respond in English unless the user explicitly asks you to use another language.

        Do not introduce yourself as Qwen.
        Do not mention Tongyi Lab.
        Do not describe your general capabilities unless asked.

        User:
        Hello! Who are you?
    """

    answer = ask_llm(text)
    print(answer)
print("hello world")
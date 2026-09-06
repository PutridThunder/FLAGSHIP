import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:1.7b"


def ask_llm(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "think": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]


def extract_intent(user_message):
    prompt = f"""
    You are the language-processing component of a personal AI assistant.

    Your job is to analyze the user's message and extract structured information.

    Always return ONLY valid JSON.
    Do not use markdown.
    Do not explain your answer.
    Do not include any text before or after the JSON.

    Use these fields:

    - intent: what the user is trying to do
    - topic: the main topic, or null if there isn't one
    - goal: what the user wants to accomplish, or null
    - project: a project mentioned by the user, or null
    - needs_resources: true if the user would benefit from finding external information, otherwise false

    User message: {user_message}
    """

    response = ask_llm(prompt)

    return json.loads(response)


if __name__ == "__main__":
    message = input("User: ")

    result = extract_intent(message)

    print(json.dumps(result, indent=4))

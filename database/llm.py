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

        Your job is to analyze the user's message and extract structured information
        that another Python program will use to decide what to do next.

        You are NOT the final conversational assistant.
        Do not answer the user's question.
        Only analyze the message and return the requested JSON.

        IMPORTANT:
        - Always return ONLY valid JSON.
        - Do not use markdown.
        - Do not explain your answer.
        - Do not include any text before or after the JSON.
        - Use double quotes for all JSON keys and string values.
        - Use null when information is not present.
        - Use true or false for needs_resources.

        Return exactly these five fields:

        1. "intent"
        The primary action or purpose of the user's message.

        Examples:
        - "hello, how are you?" → "greeting"
        - "What is a neural network?" → "answer_question"
        - "I want to learn Python." → "learn"
        - "Find tutorials for OpenCV." → "find_resources"
        - "Remember that I'm building a robotics assistant." → "store_memory"
        - "What do you remember about me?" → "retrieve_memory"

        2. "topic"
        The main subject being discussed.

        Examples:
        - "What is a neural network?" → "neural network"
        - "I want to learn Python." → "Python"
        - "I'm building a robot." → "robotics"
        - "hello, how are you?" → null

        3. "goal"
        What the user wants to accomplish, if they are trying to accomplish
        something.

        Do NOT put the project itself in the goal field.

        Examples:
        - "I want to learn computer vision for my robotics project."
            → "learn computer vision"
        - "I want to use a camera to detect objects."
            → "detect objects"
        - "I want to find Python courses."
            → "find Python courses"
        - "What is a neural network?"
            → "understand what a neural network is"
        - "My favorite language is Python."
            → null

        4. "project"
        A specific project, system, application, research project, or other
        ongoing work mentioned by the user.

        If the user describes themselves as building, developing, working on,
        creating, or maintaining something that represents an ongoing project,
        identify it here even if they do not explicitly use the word "project".

        Examples:
        - "I'm building a robotics assistant."
            → "robotics assistant"
        - "I'm building a website that helps SFU students plan their courses."
            → "SFU course planning website"
        - "I'm working on a machine learning project that predicts air quality."
            → "air quality prediction project"
        - "I want to learn Python."
            → null
        - "What is a neural network?"
            → null

        5. "needs_resources"
        Set this to true ONLY when the user is asking for, or would clearly
        benefit from, information that should be retrieved from an external
        source.

        Set this to false when the user's request can reasonably be handled
        using the assistant's existing knowledge, normal conversation, or the
        user's stored information.

        Examples:
        - "Find me tutorials for OpenCV." → true
        - "Find the best Python courses." → true
        - "What is a neural network?" → false
        - "How do AVL tree rotations work?" → false
        - "What do you remember about me?" → false
        - "Remember that I'm building a robotics assistant." → false
        - "I'm tired today." → false

        IMPORTANT DISTINCTIONS:

        - "intent" describes WHAT OPERATION the assistant should perform.
        - "topic" describes WHAT SUBJECT the message is about.
        - "goal" describes WHAT OUTCOME the user wants.
        - "project" describes an ONGOING PROJECT the user is working on.
        - "needs_resources" describes whether EXTERNAL INFORMATION RETRIEVAL is needed.

        If a message contains multiple pieces of information, extract all relevant
        information into the appropriate fields.

        Do not invent information that the user did not provide.

        User message:
        {user_message}
    """

    response = ask_llm(prompt)

    return json.loads(response)


while True:
    if __name__ == "__main__":
        message = input("User: ")

        result = extract_intent(message)

        print(json.dumps(result, indent=4))

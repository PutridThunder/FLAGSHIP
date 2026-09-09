import sqlite3
import json
from database.llm import extract_intent, store_memory, retrieve_memories

# path to our database

DATABASE = "data/assistant.db"

# connecting this file to the database

def connect_database():
    return sqlite3.connect(DATABASE)

# getting a user row by their int id

def get_user(user_id):
    
    connection = connect_database()

    # creating a cursor that executes SQL commands
    cursor = connection.cursor() 

    # using id to locate first name and last name
    cursor.execute(
        "SELECT id, first_name, last_name FROM users WHERE id = ?",
        (user_id,)
    )

    # locates by first match

    user = cursor.fetchone()

    # closes connection to the database
    connection.close()

    return user

# For now, we're using Sahib's user ID.


def handle_message(user_id, message):

    result = extract_intent(message)

    print("\nStructured information:")

    print(json.dumps(result, indent=4))

    print("Responding...")

    intent = result["intent"]

    if intent == "store_memory":

        if result["project"] is not None:
            store_memory(user_id, result["project"])
            return "Got it. I'll remember that."

        return "What would you like me to remember?"
    
    elif intent == "retrieve_memory":

        memories = retrieve_memories(user_id)

        if len(memories) == 0:
            return "I don't have any memories stored for you yet."

        response = "Here's what I remember:\n"

        for memory in memories:
            response += f"- {memory}\n"

        return response

    elif intent == "greeting":

        return "Hello!"
    
    elif intent == "goodbye":
        return "Goodbye!"

    elif intent == "answer_question":

        return "I can answer that."

    else:

        return "I don't know how to handle that yet."

if __name__ == "__main__":

    user_id = 1

    print(f"Hello, {get_user(user_id)[1]}!")

    while True:

        message = input("> ")

        if message.lower() == "quit":
            break

        print("Generating response...")
        response = handle_message(user_id, message)

        print(response)

# if user:
#     print(f"Hello, {user[1]}!")

#     while True:
#         message = input("> ")

#         if message.lower() == "quit":
#             break

#         print(f"You said: {message}")
#     else:
#         print("User not found.")
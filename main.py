import sqlite3

# path to our database

DATABASE = "data/assistant.db"

# connecting this file to the database

def connect_database():
    return sqlite3.connect(DATABASE)

# getting a user row by their int id

def get_user(user_id):
    
    connection = connect_database()

    # creating a pointer that points to a specific row
    
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

user = get_user(1)

if user:
    print(f"Hello, {user[1]}!")

    while True:
        message = input("> ")

        if message.lower() == "quit":
            break

        print(f"You said: {message}")
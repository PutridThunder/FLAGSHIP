CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
-- this initialises the design of the database, it is called users with the info given as columns

-- users will be in a table as shown
-- id | first_name | last_name | created_at | updated_at
--  1 | Sahib      | Bains     | 1:00:02    | 1:00:02


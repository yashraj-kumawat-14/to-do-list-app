import sqlite3

conn = sqlite3.connect("todoist.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    priority INT NOT NULL,
    status TEXT NOT NULL,
    date TEXT DEFAULT (CURRENT_TIMESTAMP)
)              
''')


conn.commit()
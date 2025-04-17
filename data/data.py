import sqlite3

def create_database():
    with sqlite3.connect('my_database.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MyTable (
            id INTEGER PRIMARY KEY,
            url TEXT,
            id_task TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            token TEXT NOT NULL UNIQUE,
            counter INTEGER DEFAULT 0
        )
        ''')

        conn.commit()

create_database()

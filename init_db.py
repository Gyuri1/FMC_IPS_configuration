import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Entry', 'Content for the first entry')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Entry', 'Content for the second entry')
            )

connection.commit()
connection.close()
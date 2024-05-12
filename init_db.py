import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for i in range(1, 6):
    cur.execute("INSERT INTO solved_puzzles (puzzle_id, solved) VALUES (?, ?)",
                (i, 0)
    )

connection.commit()
connection.close()

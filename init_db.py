import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for i in range(1, 6):
    solved = 0
    if i == 1:
        solved = 1
    cur.execute("INSERT INTO solved_puzzles (puzzle_id, solved) VALUES (?, ?)",
                (i, solved)
                )

connection.commit()
connection.close()

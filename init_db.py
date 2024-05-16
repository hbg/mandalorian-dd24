import sqlite3
import uuid
import string
import random

connection = sqlite3.connect('database.db')
ids = ['jydjzqpl', 'opetk0gx', 'ckkuoofn', 'vfx1p1h1',
       'ikqz56vs', 'fftthtyr', '0rau721m', 'b1nzo9t8']

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for i in range(1, 6):
    cur.execute("INSERT INTO solved_puzzles (puzzle_id, solved) VALUES (?, ?)",
                (i, 0)
    )
for i in range(8):
    cur.execute("INSERT INTO comm_status (comm_id, solved) VALUES (?, ?)", (ids[i], 0))

connection.commit()
connection.close()

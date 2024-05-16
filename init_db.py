import sqlite3
import uuid
import string
import random

def random_id():
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choices(alphabet, k=8))

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for i in range(1, 6):
    cur.execute("INSERT INTO solved_puzzles (puzzle_id, solved) VALUES (?, ?)",
                (i, 0)
    )
    cur.execute("INSERT INTO comm_status (comm_id, solved) VALUES (?, ?)", (random_id(), 1))

connection.commit()
connection.close()

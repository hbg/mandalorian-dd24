import sqlite3
from flask import Flask, render_template, request, jsonify, redirect
import os
from datetime import datetime
import configparser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'themandaloriandd24'

# Setup config
config = configparser.ConfigParser()
config.read('app.cfg')
base_url = config.get('DEFAULT', 'base_url')

codes = {
    '1': ['air', 'season', 'small', 'yoda', 'like'],
    '2': ['plant', 'plant', 'fire', 'kill'],
    '3': ['small', 'sloth', 'jedi', 'jedi', 'protect'],
    '4': ['moon', 'person', 'see'],
    '5': ['go', 'garden', 'mandalorian', 'can', 'not'],
}

code_hints = {
    str(puzzle_id) :  f'{base_url}/static/img/language_puzzles/{puzzle_id}.png'
    for puzzle_id in range(1, 6)
}

GLYPH_PATH = 'app/static/img/glyphs/'
categories = {
    category: [i.replace(".png", "") for i in os.listdir(GLYPH_PATH + category)]
    for category in ["adjectives", "nouns", "people", "places", "verbs"]
}

def get_db_connection():
    conn = sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn

def get_elapsed_seconds():
    conn = get_db_connection()
    act_times = conn.execute("SELECT strftime('%s', 'now') - strftime('%s', activation_time) AS elapsed_seconds FROM activation").fetchall()
    if len(act_times) == 0:
        return None
    conn.close()
    return act_times[0]['elapsed_seconds']

def is_solved(puzzle_id):
    conn = get_db_connection()
    stmt = 'SELECT solved FROM solved_puzzles WHERE puzzle_id=?'
    puzzles = conn.execute(stmt, (puzzle_id,)).fetchall()
    conn.close()
    if len(puzzles) == 0:
        return None
    return puzzles[0]['solved'] == 1

def get_emergency_phones():
    conn = get_db_connection()
    stmt = 'SELECT * FROM comm_status'
    phones = conn.execute(stmt).fetchall()
    conn.close()
    return phones

def get_emergency_phone(comm_id):
    conn = get_db_connection()
    stmt = 'SELECT * FROM comm_status WHERE comm_id = ?'
    phones = conn.execute(stmt, (comm_id,)).fetchall()
    conn.close()
    if len(phones) == 0:
        return None
    return phones[0]

def solve_emergency_phone(comm_id):
    conn = get_db_connection()
    stmt = 'UPDATE comm_status SET solved = ? WHERE comm_id = ?'
    conn.execute(stmt, (1, comm_id))
    conn.commit()
    conn.close()
    return

@app.route("/")
def home_view():
    elapsed_secs = get_elapsed_seconds()
    if elapsed_secs and elapsed_secs > 15 * 60:
        conn = get_db_connection()
        puzzles = conn.execute('SELECT * FROM solved_puzzles').fetchall()
        conn.close()
        return render_template('index.html', puzzles=puzzles, base_url=base_url)
    else:
        if not elapsed_secs:
            return render_template('activate.html', activated=False, base_url=base_url)
        return render_template('activate.html', activated=True, elapsed_secs=elapsed_secs, base_url=base_url)

@app.route('/comms/status')
def emergency_phones_view():
    phones = get_emergency_phones()
    return render_template('emergency_phones.html', base_url=base_url, phones=phones)

@app.route("/code/<code_id>")
def code_view(code_id):
    solved = is_solved(code_id)
    if solved is None:
        return redirect(base_url)
    print(solved)
    return render_template('code.html', code_id=code_id, code_hint=code_hints[code_id],
                           code_solution = codes[code_id], solved=solved,
                           categories=categories, base_url=base_url)

@app.route('/comms/<comm_id>')
def comm_view(comm_id, methods=['GET', 'POST']):
    if request.method == 'GET':
        comm_details = get_emergency_phone(comm_id)
        if comm_details is None:
            return redirect(base_url+'/comms/status')
        else:
            return render_template('emergency_phone_puzzle.html', details=comm_details, base_url=base_url)
    else:
        comm_details = get_emergency_phone(comm_id)
        if comm_details is None:
            return jsonify({
                "solved": False,
                "comm_id": comm_id
            })
        else:
            solved = comm_details["solution"] == request.json.get("code")
            if solved:
                solve_emergency_phone(comm_id)
            return jsonify({
                "solved": solved,
                "comm_id": comm_id
            })



@app.route("/submit", methods=["POST"])
def submit_code():
    if request.method == 'POST':
        code_id = request.json["codeId"]
        code = request.json["code"]
        soln = codes[code_id]
        solved = code == soln
        if solved:
            conn = get_db_connection()
            update_stmt = f'UPDATE solved_puzzles SET solved=? WHERE puzzle_id=?'
            conn.execute(
                update_stmt, (1, code_id)
            )
            conn.commit()
            conn.close()
        return jsonify({
            'code_id': code_id,
            'solved': solved
        })
    else:
        return home_view()

@app.route('/activate')
def activate_view():
    conn = get_db_connection()
    insert_stmt = 'INSERT INTO activation DEFAULT VALUES;'
    conn.execute(insert_stmt)
    conn.commit()
    conn.close()
    return redirect(base_url)

@app.route("/reset_progress")
def reset_progress():
    conn = get_db_connection()
    update_stmt = f'UPDATE solved_puzzles SET solved=?'
    conn.execute(
        update_stmt, (0,)
    )
    conn.commit()
    conn.close()
    return redirect(base_url)
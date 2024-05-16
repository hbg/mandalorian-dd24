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
    '1': ['moon']*5,
    '2': ['moon']*2 + ['sun']*3,
    '3': ['1','3','5','5','7'],
    '4': ['1','3','5','5','7'],
    '5': ['1','3','5','5','7'],
}

code_hints = {
    '1': 'https://helios-i.mashable.com/imagery/articles/01pkPQvUb6TvGYptPMBKR4x/hero-image.fill.size_1200x900.v1681906803.jpg',
    '2': 'https://m.media-amazon.com/images/M/MV5BMTBlNDU1NTgtNjY1Zi00ZTU0LTlkN2ItZmM5NDM5NmMyNzk3XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg',
    '3': 'https://www.dexerto.com/cdn-cgi/image/width=3840,quality=60,format=auto/https://editors.dexerto.com/wp-content/uploads/2023/04/19/the-mandalorian-season-4-1.jpg',
    '4': 'https://cdn.vox-cdn.com/thumbor/9QrnNlxvb39PlbtDfJEBqg5O6S4=/0x0:1939x706/1200x800/filters:focal(895x195:1205x505)/cdn.vox-cdn.com/uploads/chorus_image/image/72195127/Screenshot_2023_04_05_082849.0.jpg',
    '5': 'https://www.digitaltrends.com/wp-content/uploads/2023/02/mandalorian-season-3-poster1.jpg?fit=720%2C421&p=1'
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
    return render_template('emergency_phones.html', base_url=base_url)

@app.route("/code/<code_id>")
def code_view(code_id):
    solved = is_solved(code_id)
    if solved is None:
        return redirect(base_url)
    print(solved)
    return render_template('code.html', code_id=code_id, code_hint=code_hints[code_id],
                           code_solution = codes[code_id], solved=solved,
                           categories=categories, base_url=base_url)

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
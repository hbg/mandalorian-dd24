import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'themandaloriandd24'
codes = {
    1: ['1','3','5','5','7'],
    2: ['1','3','5','5','7'],
    3: ['1','3','5','5','7'],
    4: ['1','3','5','5','7'],
    5: ['1','3','5','5','7'],
}

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home_view():
    conn = get_db_connection()
    puzzles = conn.execute('SELECT * FROM solved_puzzles').fetchall()
    conn.close()
    return render_template('index.html', puzzles=puzzles)

@app.route("/code/<code_id>")
def code_view(code_id):
    return render_template('code.html', code_id=code_id, code_solution='hello')

@app.route("/submit", methods=["POST"])
def submit_code():
    if request.method == 'POST':
        code_id = request.json["codeId"]
        code = request.json["code"]
        soln = codes[int(code_id)]
        solved = code == soln
        if solved:
            print("Hello")
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
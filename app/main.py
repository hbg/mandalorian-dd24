
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_view():
    return render_template('index.html')

@app.route("/code/<code_id>")
def code_view(code_id):
    return render_template('code.html', code_id=code_id)
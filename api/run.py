from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    return render_template('index.html', message="Here is a message")

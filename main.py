from flask import Flask, url_for
from flask.templating import render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/hello')
def hello_world():
    return 'Hello, World!'
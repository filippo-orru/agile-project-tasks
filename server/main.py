# Tutorial: https://flask.palletsprojects.com/en/1.1.x/quickstart/
from flask import Flask, jsonify, request
from flask.templating import render_template
from server.db_conn import DatabaseConnection

database = DatabaseConnection()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/print')
def print():
    return render_template('print.html')


@app.route('/api/tasks', methods=["GET"])
def tasks_get():
    offset = 0
    offsetStr = request.args.get('offset')
    if offsetStr and offsetStr != '':
        offset = int(offsetStr)

    limit = 10
    limitStr = request.args.get('limit')
    if limitStr and limitStr != '':
        limit = int(limitStr)

    tasks, more = database.get_tasks(offset, limit)

    return jsonify({
        "offset": offset,
        "limit": limit,
        "more": more,
        "tasks": tasks
    })


@app.route('/api/tasks', methods=["POST"])
def tasks_post():
    return

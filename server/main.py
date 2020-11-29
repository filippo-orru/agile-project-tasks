# Tutorial: https://flask.palletsprojects.com/en/1.1.x/quickstart/

from server.collections import Task
from flask import Flask, jsonify, request
from flask.templating import render_template
from server.database_connection import DatabaseConnection

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

    tasks, more = database.collections.tasks.get_many(offset, limit)

    return jsonify({
        "offset": offset,
        "limit": limit,
        "more": more,
        "tasks": tasks
    })


@app.route('/api/tasks', methods=["POST"])
def tasks_post():
    task = Task.fromJson(request.json)
    task = database.collections.tasks.insert(task)

    return jsonify(task)


@app.route('/api/tasks/<id>', methods=["GET"])
def tasks_get_id(id: str):
    task = database.collections.tasks.get(int(id))
    return jsonify(task.serialize())
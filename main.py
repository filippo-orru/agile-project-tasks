# Tutorial: https://flask.palletsprojects.com/en/1.1.x/quickstart/

from server.validator import Validator
from server.collections import Collections, Task
from flask import Flask, jsonify, request, redirect
from flask.templating import render_template
from server.database_connection import DatabaseConnection

db = DatabaseConnection()

collections = Collections(db)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/print')
def print():
    return render_template('print.html')


@app.route('/add_task')
def add_task():
    return render_template('add_task.html')


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

    tasks, more = collections.tasks.get_many(offset, limit)

    tasks = list(map(lambda task: task.toDict(), tasks))

    return jsonify({
        "offset": offset,
        "limit": limit,
        "more": more,
        "tasks": tasks
    })


@app.route('/api/tasks', methods=["POST"])
def tasks_post():
    task = Task.fromJson(request.json)
    # returnMsg = Validator.task_validate(task)

    # if returnMsg == "success":
    #     returnMsg = "succ"
    task = collections.tasks.insert(task)

    return jsonify(task.toDict())


@app.route('/api/tasks/<id>', methods=["GET"])
def tasks_get_id(id: str):
    task = collections.tasks.get(int(id))
    if task is None:
        return "Not found", 404
    else:
        return jsonify(task.toDict())

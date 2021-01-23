# Flask tutorial: https://flask.palletsprojects.com/en/1.1.x/quickstart/

from flask.helpers import make_response
from server.collections import Collections, Task
from flask import Flask, jsonify, request
from flask.templating import render_template
from server.database_connection import DatabaseConnection
import pdfkit

db = DatabaseConnection()

collections = Collections(db)

app = Flask(__name__)

####  Start: General  vvvv


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/print')
def print():
    return render_template('print.html')


@app.route('/tasks/add')
def tasks_add():
    return render_template('add_task.html')


@app.route('/tasks/download')
def tasks_download():
    tasks, _ = collections.tasks.get_many(0, limit=-1)
    all_tasks = list(map(lambda task: task.toDict(formatHumanTime=True),
                         tasks))
    htmlString = render_template('pdf_template.jinja2', tasks=all_tasks)

    pdf = pdfkit.from_string(str(htmlString),
                             output_path=False,
                             options={
                                 'quiet': '',
                                 'enable-local-file-access': '',
                                 'default-header': '',
                                 'header-left': 'Agile Manager - All tasks',
                                 'header-line': '',
                             })
    response = make_response()
    response.data = pdf
    response.headers['Content-Type'] = 'application/pdf'
    return response


####  Start: API  vvvv


@app.route('/api/tasks', methods=["GET"])
def tasks_get():
    searchFilter = request.args.get('search')
    offset = 0
    offsetStr = request.args.get('offset')
    if offsetStr and offsetStr != '':
        offset = int(offsetStr)

    limit = 10
    limitStr = request.args.get('limit')
    if limitStr and limitStr != '':
        limit = int(limitStr)

    tasks, more = collections.tasks.get_many(offset, limit, searchFilter)

    tasks = list(map(lambda task: task.toDict(), tasks))

    return jsonify({
        "offset": offset,
        "limit": limit,
        "more": more,
        "tasks": tasks,
        "search": searchFilter
    })


@app.route('/api/tasks', methods=["POST"])
def tasks_post():
    task = Task.fromJson(request.json)
    returnMsg = task.validate()

    if "success" in returnMsg:
        task = collections.tasks.insert(task)

    return jsonify(returnMsg)


@app.route('/api/tasks/<id>', methods=["GET"])
def tasks_get_id(id: str):
    task = collections.tasks.get(int(id))
    if task is None:
        return "Not found", 404
    else:
        return jsonify(task.toDict())

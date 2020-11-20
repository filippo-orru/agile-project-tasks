from flask import Flask, url_for, jsonify, request
from flask.templating import render_template
import json

# read test data
with open('resources/test_data.json', 'r') as testDataFile:
    data = testDataFile.read()

testData = json.loads(data)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/print')
def print():
    return render_template('print.html')


@app.route('/tasks')
def tasks():
    offset = 0
    offsetStr = request.args.get('offset')
    if offsetStr and offsetStr != '':
        offset = int(offsetStr)

    limit = 10
    limitStr = request.args.get('limit')
    if limitStr and limitStr != '':
        limit = int(limitStr)

    if limit == -1:
        subset = testData
    elif offset + limit <= len(testData):
        subset = testData[offset:offset + limit]
    elif offset <= len(testData):
        subset = testData[offset:]
    else:
        subset = []

    return jsonify({
        "offset": offset,
        "limit": limit,
        "more": len(testData) > limit + offset,
        "tasks": subset
    })

import json

from flask import Flask
from flask import jsonify
from gevent.pywsgi import WSGIServer

from Database import Database

app = Flask(__name__)

with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

database = Database(SETTINGS["database"])


@app.route('/')
def index():
    return ""


@app.route('/roadmaps', methods=['GET'])
def get_roadmaps():
    return jsonify(database.get_roadmaps())


@app.route('/roadmap/<int:roadmapID>', methods=['GET'])
def get_roadmap_name(roadmapID):
    return jsonify(database.get_roadmap_name(roadmapID))


@app.route('/milestones/<int:roadmapID>', methods=['GET'])
def get_milestones(roadmapID):
    return jsonify(database.get_milestones(roadmapID))


@app.route('/milestones/<int:roadmapID>/open', methods=['GET'])
def get_open_milestones(roadmapID):
    return jsonify(database.get_open_milestones(roadmapID))


@app.route('/milestone/<int:milestoneID>', methods=['GET'])
def get_milestone(milestoneID):
    return jsonify(database.get_milestone(milestoneID))


@app.route('/tasks/<int:milestoneID>', methods=['GET'])
def get_tasks(milestoneID):
    return jsonify(database.get_tasks(milestoneID))


@app.route('/tasks/<int:milestoneID>/open', methods=['GET'])
def get_open_tasks(milestoneID):
    return jsonify(database.get_open_tasks(milestoneID))


@app.route('/task/<int:taskID>', methods=['GET'])
def get_task(taskID):
    return jsonify(database.get_task(taskID))


@app.route('/subtasks/<int:taskID>', methods=['GET'])
def get_sub_tasks(taskID):
    return jsonify(database.get_sub_tasks(taskID))


@app.route('/subtasks/<int:taskID>/open', methods=['GET'])
def get_open_sub_tasks(taskID):
    return jsonify(database.get_open_sub_tasks(taskID))


@app.route('/subtask/<int:subTaskID>', methods=['GET'])
def get_sub_task(subTaskID):
    return jsonify(database.get_sub_task(subTaskID))


if __name__ == "__main__":
    serverSettings = SETTINGS["server"]
    if serverSettings["useSSL"]:
        http_server = WSGIServer((serverSettings["listen"], serverSettings["port"]), app, keyfile=serverSettings["keyfile"], certfile=serverSettings["certfile"])
    else:
        http_server = WSGIServer((serverSettings["listen"], serverSettings["port"]), app)

    http_server.serve_forever()

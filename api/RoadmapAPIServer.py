import json

from datetime import datetime
from flask import Flask, send_from_directory, request
from flask import jsonify
from gevent.pywsgi import WSGIServer

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from Database import Database
from UserService import UserService

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "KulYdiZJTEvUxNKyseaX"
jwt = JWTManager(app)

with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

database = Database(SETTINGS["database"])
userService = UserService(SETTINGS["users"])

SERVER_SETTINGS = SETTINGS["server"]
DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)


@app.route('/')
def index():
    return send_from_directory("docs", "api.html")


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None:
        return jsonify({"msg": "Missing username parameter"}), 400
    if password is None:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = userService.get_password_by_username(username)
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


"""
ROADMAPS 
"""
@app.route('/roadmaps', methods=['GET'])
def get_roadmaps():
    return jsonify(database.get_roadmaps())


@app.route('/roadmap/<int:roadmapID>', methods=['GET'])
def get_roadmap(roadmapID):
    return jsonify(database.get_roadmap(roadmapID))


@app.route('/roadmap/<int:roadmapID>/full', methods=['GET'])
def get_roadmap_fast(roadmapID):
    roadmap = database.get_roadmap(roadmapID)
    roadmap["milestones"] = database.get_milestones(roadmapID)

    numberOfOpenMilestones = 0
    for milestone in roadmap["milestones"]:
        if milestone["DueDate"] == DEFAULT_DATE:
            milestone["DueDate"] = "-"
        else:
            milestone["DueDate"] = datetime.strftime(milestone["DueDate"], "%d.%m.%Y")

        if milestone["CompletionDate"] == DEFAULT_DATE:
            milestone["CompletionDate"] = "-"
        else:
            milestone["CompletionDate"] = datetime.strftime(milestone["CompletionDate"], "%d.%m.%Y")

        if milestone["Status"] == 0:
            numberOfOpenMilestones += 1

        milestone["tasks"] = database.get_tasks(milestone["ID"])

        numberOfOpenTasks = 0
        for task in milestone["tasks"]:
            task["subtasks"] = database.get_sub_tasks(task["ID"])

            numberOfOpenSubTasks = 0
            for subtask in task["subtasks"]:
                if subtask["Status"] == 0:
                    numberOfOpenSubTasks += 1
            task["numberOfOpenSubTasks"] = numberOfOpenSubTasks

            if task["Status"] == 0:
                numberOfOpenTasks += 1
        milestone["numberOfOpenTasks"] = numberOfOpenTasks

    roadmap["numberOfOpenMilestones"] = numberOfOpenMilestones
    return jsonify(roadmap)


"""
MILESTONES 
"""
@app.route('/milestones/<int:roadmapID>', methods=['GET'])
def get_milestones(roadmapID):
    return jsonify(database.get_milestones(roadmapID))


@app.route('/milestones/<int:roadmapID>/open', methods=['GET'])
def get_open_milestones(roadmapID):
    return jsonify(database.get_open_milestones(roadmapID))


@app.route('/milestones/<int:roadmapID>/latest', methods=['GET'])
def get_latest_milestone(roadmapID):
    return jsonify(database.get_latest_milestone(roadmapID))


@app.route('/milestone/<int:milestoneID>', methods=['GET'])
def get_milestone(milestoneID):
    return jsonify(database.get_milestone(milestoneID))


@app.route('/admin', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


""" 
TASKS 
"""
@app.route('/tasks/<int:milestoneID>', methods=['GET'])
def get_tasks(milestoneID):
    return jsonify(database.get_tasks(milestoneID))


@app.route('/tasks/<int:milestoneID>/open', methods=['GET'])
def get_open_tasks(milestoneID):
    return jsonify(database.get_open_tasks(milestoneID))


@app.route('/task/<int:taskID>', methods=['GET'])
def get_task(taskID):
    return jsonify(database.get_task(taskID))


""" 
SUBTASKS 
"""
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
    if SERVER_SETTINGS["useSSL"]:
        http_server = WSGIServer((SERVER_SETTINGS["listen"], SERVER_SETTINGS["port"]), app,
                                 keyfile=SERVER_SETTINGS["keyfile"], certfile=SERVER_SETTINGS["certfile"])
    else:
        http_server = WSGIServer((SERVER_SETTINGS["listen"], SERVER_SETTINGS["port"]), app)

    http_server.serve_forever()

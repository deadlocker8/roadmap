import json

from flask import Flask, send_from_directory, request
from flask import jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token
)
from gevent.pywsgi import WSGIServer

from Database import Database
from RequestValidator import RequestValidator, ValidationError
from UserService import UserService
from blueprints import SubTaskAPI, MilestoneAPI, TaskAPI, RoadmapAPI

with open("settings.json", "r") as f:
    SETTINGS = json.load(f)
SERVER_SETTINGS = SETTINGS["server"]

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = SERVER_SETTINGS["secret"]
jwt = JWTManager(app)

database = Database(SETTINGS["database"])
userService = UserService(SETTINGS["users"])


@app.route('/')
def index():
    return send_from_directory("docs", "api.html")


@app.route('/version', methods=['GET'])
def version():
    with open("version.json", "r") as f:
        return jsonify(json.load(f)["version"])


@app.route('/login', methods=['POST'])
def login():
    try:
        parameters = RequestValidator.validate(request, ["username", "password"])
    except ValidationError as e:
        return e.response, 400

    password = userService.get_password_by_username(parameters["username"])
    if password is None:
        return jsonify({"success": False, "msg": "Unknown username"}), 401

    if password != parameters["password"]:
        return jsonify({"success": False, "msg": "Bad credentials"}), 401

    access_token = create_access_token(identity=parameters["username"])
    return jsonify(access_token=access_token), 200


app.register_blueprint(RoadmapAPI.construct_blueprint(database))
app.register_blueprint(MilestoneAPI.construct_blueprint(database))
app.register_blueprint(TaskAPI.construct_blueprint(database))
app.register_blueprint(SubTaskAPI.construct_blueprint(database))


if __name__ == "__main__":
    if SERVER_SETTINGS["useSSL"]:
        http_server = WSGIServer((SERVER_SETTINGS["listen"], SERVER_SETTINGS["port"]), app,
                                 keyfile=SERVER_SETTINGS["keyfile"], certfile=SERVER_SETTINGS["certfile"])
    else:
        http_server = WSGIServer((SERVER_SETTINGS["listen"], SERVER_SETTINGS["port"]), app)

    print('Listening on {}:{}...'.format(SERVER_SETTINGS['listen'], SERVER_SETTINGS['port']))
    http_server.serve_forever()

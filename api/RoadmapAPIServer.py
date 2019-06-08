import json

from flask import Flask, send_from_directory, request
from flask import jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from gevent.pywsgi import WSGIServer

from RequestValidator import RequestValidator, ValidationError
from blueprints import SubTaskAPI, MilestoneAPI, TaskAPI, RoadmapAPI
from Database import Database
from UserService import UserService

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


@app.route('/admin', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    if SERVER_SETTINGS["useSSL"]:
        http_server = WSGIServer((SERVER_SETTINGS["listen"], SERVER_SETTINGS["port"]), app,
                                 keyfile=SERVER_SETTINGS["keyfile"], certfile=SERVER_SETTINGS["certfile"])
    else:
        http_server = WSGIServer((SERVER_SETTINGS["listen"], SERVER_SETTINGS["port"]), app)

    http_server.serve_forever()

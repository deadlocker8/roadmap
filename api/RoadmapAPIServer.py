import datetime
import json
import logging
import os

import yaml
from TheCodeLabs_BaseUtils.DefaultLogger import DefaultLogger
from TheCodeLabs_FlaskUtils import FlaskBaseApp
from flask import jsonify, render_template
from flask import request
from flask_jwt_extended import (
    JWTManager, create_access_token
)

from blueprints import SubTaskAPI, MilestoneAPI, TaskAPI, RoadmapAPI
from logic import Constants
from logic.Database import Database
from logic.RequestValidator import RequestValidator, ValidationError
from logic.UserService import UserService

LOGGER = DefaultLogger().create_logger_if_not_exists(Constants.APP_NAME)


class RoadmapApi(FlaskBaseApp):
    def __init__(self, appName: str, rootDir: str, logger: logging.Logger, settingsPath: str):
        super().__init__(appName, rootDir, logger, settingsPath=settingsPath, serveFavicon=False)
        self._database = Database(self._settings['database'])
        self._userService = UserService(self._settings['users'])

    def _register_blueprints(self, app):
        app.config['JWT_SECRET_KEY'] = self._serverSettings['secret']
        jwt = JWTManager(app)

        @app.route('/')
        def index():
            yamlPath = os.path.join(Constants.ROOT_DIR, 'docs', 'api.yml')
            with open(yamlPath, 'r') as yamlFile:
                specification = yaml.load(yamlFile, Loader=yaml.FullLoader)

            specification['servers'][0]['url'] = self._settings['api']['url']
            specification['info']['version'] = self._version['name']

            specification = json.dumps(specification)
            return render_template('api.html', appName="Roadmaps", openApiSpecification=specification)

        @app.route('/login', methods=['POST'])
        def login():
            try:
                parameters = RequestValidator.validate(request, ['username', 'password'])
            except ValidationError as e:
                return e.response, 400

            password = self._userService.get_password_by_username(parameters['username'])
            if password is None:
                return jsonify({'success': False, 'msg': 'Unknown username'}), 401

            if password != parameters['password']:
                return jsonify({'success': False, 'msg': 'Bad credentials'}), 401

            expires = datetime.timedelta(hours=1)
            access_token = create_access_token(identity=parameters['username'], expires_delta=expires)
            return jsonify(access_token=access_token), 200

        app.register_blueprint(RoadmapAPI.construct_blueprint(self._database))
        app.register_blueprint(MilestoneAPI.construct_blueprint(self._database))
        app.register_blueprint(TaskAPI.construct_blueprint(self._database))
        app.register_blueprint(SubTaskAPI.construct_blueprint(self._database))


if __name__ == '__main__':
    roadmapApi = RoadmapApi(Constants.APP_NAME, os.path.dirname(__file__), LOGGER, 'settings.json')
    roadmapApi.start_server()

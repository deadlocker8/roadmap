import logging
import os
from datetime import datetime

import requests
from TheCodeLabs_BaseUtils.DefaultLogger import DefaultLogger
from TheCodeLabs_FlaskUtils import FlaskBaseApp
from flask import render_template, redirect, session

from logic import Constants
from logic.Localization import LOCALIZATION
from logic.UrlBuilder import UrlBuilder
from blueprints import Roadmaps, Authentication, Milestones, Tasks, SubTasks

LOGGER = DefaultLogger().create_logger_if_not_exists(Constants.APP_NAME)


class RoadmapClient(FlaskBaseApp):
    DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)

    def __init__(self, appName: str, rootDir: str, logger: logging.Logger, settingsPath: str):
        super().__init__(appName, rootDir, logger, settingsPath=settingsPath)
        self._urlBuilder = UrlBuilder(self._serverSettings['apiURL'])

    def _register_blueprints(self, app):
        app.register_blueprint(Authentication.construct_blueprint(self._urlBuilder))
        app.register_blueprint(Roadmaps.construct_blueprint(self._urlBuilder))
        app.register_blueprint(Milestones.construct_blueprint(self._urlBuilder))
        app.register_blueprint(Tasks.construct_blueprint(self._urlBuilder))
        app.register_blueprint(SubTasks.construct_blueprint(self._urlBuilder))

        @app.route('/')
        def overview():
            roadmaps = requests.get(self._urlBuilder.build_url('roadmaps')).json()
            return render_template('overview.html', roadmaps=roadmaps)

        @app.route('/roadmap/')
        def roadmap():
            return redirect('/')

        @app.route('/roadmap/<roadmapID>')
        def roadmap_by_id(roadmapID):
            success, response = self.__check_roadmap(roadmapID, self._urlBuilder)
            if success:
                return render_template('index.html', roadmap=response, localization=LOCALIZATION)

            return response

        @app.route('/roadmap/<roadmapID>/fragment')
        def roadmap_fragment_by_id(roadmapID):
            success, response = self.__check_roadmap(roadmapID, self._urlBuilder)
            if success:
                return render_template('roadmapFragment.html', roadmap=response, localization=LOCALIZATION)

            return response

    @staticmethod
    def __check_roadmap(roadmapID, urlBuilder):
        try:
            roadmapID = int(roadmapID)
        except ValueError:
            return False, render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        if roadmapID < 1:
            return False, render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        headers = {}
        if session:
            headers = {'Authorization': 'Bearer  {}'.format(session['session_token'])}

        response = requests.get(urlBuilder.build_url('roadmap', roadmapID, 'full'), headers=headers)
        if response.status_code != 200:
            return False, render_template('error.html', message=LOCALIZATION['error_roadmap_not_existing'])

        roadmap = response.json()
        if roadmap is None:
            return False, render_template('error.html', message=LOCALIZATION['error_roadmap_not_existing'])

        return True, roadmap


if __name__ == '__main__':
    roadmapClient = RoadmapClient(Constants.APP_NAME, os.path.dirname(__file__), LOGGER, 'settings.json')
    roadmapClient.start_server()

import json
from datetime import datetime

import requests
from flask import Flask, render_template, redirect
from gevent.pywsgi import WSGIServer

from Localization import LOCALIZATION
from UrlBuilder import UrlBuilder
from blueprints import Roadmaps, Authentication, Milestones, Tasks, SubTasks

with open('settings.json', 'r') as f:
    SETTINGS = json.load(f)

app = Flask(__name__)
app.secret_key = SETTINGS['secret']

DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)

URL_BUILDER = UrlBuilder(SETTINGS['apiURL'])

app.register_blueprint(Authentication.construct_blueprint(URL_BUILDER))
app.register_blueprint(Roadmaps.construct_blueprint(URL_BUILDER))
app.register_blueprint(Milestones.construct_blueprint(URL_BUILDER))
app.register_blueprint(Tasks.construct_blueprint(URL_BUILDER))
app.register_blueprint(SubTasks.construct_blueprint(URL_BUILDER))


@app.route('/')
def overview():
    roadmaps = requests.get(URL_BUILDER.build_url('roadmaps')).json()
    return render_template('overview.html', roadmaps=roadmaps)


@app.route('/roadmap/')
def roadmap():
    return redirect('/')


@app.route('/roadmap/<roadmapID>')
def roadmap_by_id(roadmapID):
    try:
        roadmapID = int(roadmapID)
    except ValueError:
        return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

    if roadmapID < 1:
        return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

    roadmap = requests.get(URL_BUILDER.build_url('roadmap', roadmapID, 'full')).json()
    if roadmap is None:
        return render_template('error.html', message=LOCALIZATION['error_roadmap_not_existing'])

    return render_template('index.html', roadmap=roadmap, localization=LOCALIZATION)


@app.route('/roadmap/<roadmapID>/fragment')
def roadmap_fragement_by_id(roadmapID):
    try:
        roadmapID = int(roadmapID)
    except ValueError:
        return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

    if roadmapID < 1:
        return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

    roadmap = requests.get(URL_BUILDER.build_url('roadmap', roadmapID, 'full')).json()
    if roadmap is None:
        return render_template('error.html', message=LOCALIZATION['error_roadmap_not_existing'])

    return render_template('roadmapFragment.html', roadmap=roadmap, localization=LOCALIZATION)


if __name__ == '__main__':
    if SETTINGS['useSSL']:
        http_server = WSGIServer((SETTINGS['listen'],
                                  SETTINGS['port']), app,
                                 keyfile=SETTINGS['keyfile'],
                                 certfile=SETTINGS['certfile'])
    else:
        http_server = WSGIServer((SETTINGS['listen'], SETTINGS['port']), app)

    print('Listening on {}:{}...'.format(SETTINGS['listen'], SETTINGS['port']))
    http_server.serve_forever()

import json
from datetime import datetime

import requests
from flask import Flask, render_template, redirect, request, session, url_for
from gevent.pywsgi import WSGIServer

from AdminWrapper import require_api_token
from Localization import LOCALIZATION
from UrlBuilder import UrlBuilder
from blueprints import Roadmaps

with open('settings.json', 'r') as f:
    SETTINGS = json.load(f)

app = Flask(__name__)
app.secret_key = SETTINGS['secret']

DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)

URL_BUILDER = UrlBuilder(SETTINGS['apiURL'])


app.register_blueprint(Roadmaps.construct_blueprint(URL_BUILDER))


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


@app.route('/admin/login')
def login():
    return render_template('login.html')


@app.route('/admin/login', methods=['POST'])
def loginPost():
    password = request.form.get('password')
    if not password:
        return redirect('/admin/login')

    jsonData = {'username': 'admin', 'password': password}

    response = requests.post(URL_BUILDER.build_url('login'), json=jsonData)

    if response.status_code == 401:
        return render_template('login.html', message=LOCALIZATION['unauthorized'])

    if response.status_code == 200:
        token = response.json()["access_token"]
        session['session_token'] = token
        return redirect(url_for('admin_roadmaps.overview'))

    return render_template('error.html', message=response.json()["msg"])


@app.route('/admin/logout')
def logout():
    del session['session_token']
    return redirect('/')


@app.route('/admin/milestones')
@require_api_token
def milestone_overview():
    return redirect('/')


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

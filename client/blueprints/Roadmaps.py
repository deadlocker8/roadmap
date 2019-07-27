import requests
from flask import Blueprint, render_template, redirect, url_for, request, session

from Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    roadmaps = Blueprint('admin_roadmaps', __name__)

    @roadmaps.route('/admin/roadmaps/overview', methods=['GET'])
    def overview():
        roadmaps = requests.get(urlBuilder.build_url('roadmaps')).json()
        return render_template('admin/roadmaps/overview.html', roadmaps=roadmaps)

    @roadmaps.route('/admin/roadmaps/add', methods=['GET'])
    def add():
        return render_template('admin/roadmaps/add.html')

    @roadmaps.route('/admin/roadmaps/edit', methods=['GET'])
    def edit():
        ID = request.args.get('ID')
        if not ID or ID < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        roadmap = requests.get(urlBuilder.build_url('roadmap', ID)).json()
        return render_template('admin/roadmaps/edit.html', roadmap=roadmap)

    @roadmaps.route('/admin/roadmaps/delete', methods=['GET'])
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        response = requests.delete(urlBuilder.build_url('roadmap', ID),
                                   headers={'Authorization': 'Bearer  {}'.format( session['session_token'])})
        if response.status_code != 200:
            return render_template('error.html', message='{}: {}'.format(LOCALIZATION['error_general'],
                                                                         response.json()['msg']))

        return redirect(url_for('overview'))

    return roadmaps

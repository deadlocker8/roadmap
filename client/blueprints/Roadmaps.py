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
        return render_template('admin/roadmaps/edit.html',
                               title='New Roadmap',
                               form_url=url_for('admin_roadmaps.add_post'))

    @roadmaps.route('/admin/roadmaps/add', methods=['POST'])
    def add_post():
        success, response = __send_api_request(urlBuilder.build_url('roadmap'),
                                               requests.post,
                                               ['Projectname'], request.form)
        if not success:
            return response
        return redirect(url_for('admin_roadmaps.overview'))

    @roadmaps.route('/admin/roadmaps/edit', methods=['GET'])
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        roadmap = requests.get(urlBuilder.build_url('roadmap', ID)).json()
        roadmap['ID'] = ID
        return render_template('admin/roadmaps/edit.html',
                               title='Edit Roadmap',
                               roadmap=roadmap,
                               form_url=url_for('admin_roadmaps.edit_post'))

    @roadmaps.route('/admin/roadmaps/edit', methods=['POST'])
    def edit_post():
        success, response = __send_api_request(urlBuilder.build_url('roadmap'),
                                               requests.put,
                                               ['ID', 'Projectname'],
                                               request.form)

        if not success:
            return response
        return redirect(url_for('admin_roadmaps.overview'))

    @roadmaps.route('/admin/roadmaps/delete', methods=['GET'])
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = __send_api_request(urlBuilder.build_url('roadmap', ID), requests.delete, [], {})
        if not success:
            return response
        return redirect(url_for('admin_roadmaps.overview'))

    def __send_api_request(url, method, argNames, formArgs):
        jsonData = {}
        for name in argNames:
            jsonData[name] = formArgs.get(name)

        response = method(url, json=jsonData, headers={'Authorization': 'Bearer  {}'.format(session['session_token'])})
        if response.status_code != 200:
            return False, render_template('error.html', message='{}: {}'.format(LOCALIZATION['error_general'],
                                                                                response.json()['msg']))
        return True, response.json()

    return roadmaps

import requests
from flask import Blueprint, render_template, redirect, url_for, request, session

from ApiRequest import ApiRequest
from Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    milestones = Blueprint('admin_milestones', __name__)

    @milestones.route('/admin/milestones/overview', methods=['GET'])
    def overview():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        milestones = requests.get(urlBuilder.build_url('milestones', ID)).json()
        return render_template('admin/milestones/overview.html', milestones=milestones)

    @milestones.route('/admin/milestones/add', methods=['GET'])
    def add():
        return render_template('admin/milestones/edit.html',
                               title='New Milestone',
                               form_url=url_for('admin_milestones.add_post'))

    @milestones.route('/admin/milestones/add', methods=['POST'])
    def add_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone'),
                                                        requests.post, request.form,
                                                        ['RoadmapID', 'VersionCode', 'VersionName', 'Title', 'DueDate',
                                                         'CompletionDate', ])
        if not success:
            return response
        return redirect(url_for('admin_milestones.overview'))

    @milestones.route('/admin/milestones/edit', methods=['GET'])
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        roadmap = requests.get(urlBuilder.build_url('roadmap', ID)).json()
        roadmap['ID'] = ID
        return render_template('admin/milestones/edit.html',
                               title='Edit Milestone',
                               roadmap=roadmap,
                               form_url=url_for('admin_milestones.edit_post'))

    @milestones.route('/admin/milestones/edit', methods=['POST'])
    def edit_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone'),
                                                        requests.post, request.form,
                                                        ['ID', 'Projectname'])

        if not success:
            return response
        return redirect(url_for('admin_milestones.overview'))

    @milestones.route('/admin/milestones/delete', methods=['GET'])
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone', ID), requests.delete, {}, [])
        if not success:
            return response
        return redirect(url_for('admin_milestones.overview'))

    return milestones

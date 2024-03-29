from datetime import datetime

import requests
from flask import Blueprint, render_template, redirect, url_for, request

from logic.AdminWrapper import require_api_token
from logic.ApiRequest import ApiRequest
from logic.Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    milestones = Blueprint('admin_milestones', __name__)

    DATE_FORMAT_API = '%d.%m.%Y'
    DATE_FORMAT_INPUT_FIELD = '%Y-%m-%d'

    @milestones.route('/admin/milestones/overview', methods=['GET'])
    @require_api_token
    def overview():
        roadmap_ID = request.args.get('roadmap_ID')
        if not roadmap_ID or int(roadmap_ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        _, roadmap = ApiRequest.send_api_request(urlBuilder.build_url('roadmap', roadmap_ID), requests.get, {}, [])
        milestones = requests.get(urlBuilder.build_url('milestones', roadmap_ID)).json()
        return render_template('admin/milestones/overview.html', milestones=milestones, roadmap=roadmap)

    @milestones.route('/admin/milestones/add', methods=['GET'])
    @require_api_token
    def add():
        return render_template('admin/milestones/edit.html',
                               title='New Milestone',
                               roadmap_ID=request.args.get('roadmap_ID'),
                               form_url=url_for('admin_milestones.add_post'))

    @milestones.route('/admin/milestones/add', methods=['POST'])
    @require_api_token
    def add_post():
        params = dict(request.form)
        params['Status'] = '1' if 'Status' in params else '0'

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone'),
                                                        requests.post, params,
                                                        [('RoadmapID', int), ('VersionCode', int), ('VersionName', str),
                                                         ('Title', str), ('DueDate', str), ('CompletionDate', str),
                                                         ('Status', int)])
        if not success:
            return response
        return redirect(url_for('admin_milestones.overview', roadmap_ID=request.form.get('RoadmapID')))

    @milestones.route('/admin/milestones/edit', methods=['GET'])
    @require_api_token
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        milestone = requests.get(urlBuilder.build_url('milestone', ID)).json()
        if milestone['DueDate'] == '-':
            milestone['DueDate'] = ''
        else:
            milestone['DueDate'] = datetime.strptime(milestone['DueDate'], DATE_FORMAT_API).strftime(
                DATE_FORMAT_INPUT_FIELD)

        if milestone['CompletionDate'] == '-':
            milestone['CompletionDate'] = ''
        else:
            milestone['DueDate'] = datetime.strptime(milestone['CompletionDate'], DATE_FORMAT_API).strftime(
                DATE_FORMAT_INPUT_FIELD)

        return render_template('admin/milestones/edit.html',
                               title='Edit Milestone',
                               roadmap_ID=request.args.get('roadmap_ID'),
                               milestone=milestone,
                               form_url=url_for('admin_milestones.edit_post'))

    @milestones.route('/admin/milestones/edit', methods=['POST'])
    @require_api_token
    def edit_post():
        params = dict(request.form)
        params['Status'] = '1' if 'Status' in params else '0'

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone'),
                                                        requests.put, params,
                                                        [('ID', int), ('RoadmapID', int), ('VersionCode', int),
                                                         ('VersionName', str), ('Title', str), ('DueDate', str),
                                                         ('CompletionDate', str), ('Status', int)])

        if not success:
            return response
        return redirect(url_for('admin_milestones.overview', roadmap_ID=params['RoadmapID']))

    @milestones.route('/admin/milestones/delete', methods=['GET'])
    @require_api_token
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone', ID), requests.delete, {}, [])
        if not success:
            return response
        return redirect(url_for('admin_milestones.overview', roadmap_ID=request.args.get('roadmap_ID')))

    return milestones

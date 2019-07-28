import requests
from flask import Blueprint, render_template, redirect, url_for, request, session

from ApiRequest import ApiRequest
from Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    milestones = Blueprint('admin_milestones', __name__)

    @milestones.route('/admin/milestones/overview', methods=['GET'])
    def overview():
        roadmap_ID = request.args.get('roadmap_ID')
        if not roadmap_ID or int(roadmap_ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        milestones = requests.get(urlBuilder.build_url('milestones', roadmap_ID)).json()
        return render_template('admin/milestones/overview.html', milestones=milestones, roadmap_ID=roadmap_ID)

    @milestones.route('/admin/milestones/add', methods=['GET'])
    def add():
        return render_template('admin/milestones/edit.html',
                               title='New Milestone',
                               roadmap_ID=request.args.get('roadmap_ID'),
                               form_url=url_for('admin_milestones.add_post'))

    @milestones.route('/admin/milestones/add', methods=['POST'])
    def add_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone'),
                                                        requests.post, request.form,
                                                        ['RoadmapID', 'VersionCode', 'VersionName',
                                                         'Title', 'DueDate', 'CompletionDate', 'Status'])
        if not success:
            return response
        return redirect(url_for('admin_milestones.overview', roadmap_ID=request.form.get('RoadmapID')))

    @milestones.route('/admin/milestones/edit', methods=['GET'])
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        milestone = requests.get(urlBuilder.build_url('milestone', ID)).json()
        return render_template('admin/milestones/edit.html',
                               title='Edit Milestone',
                               milestone=milestone,
                               form_url=url_for('admin_milestones.edit_post'))

    @milestones.route('/admin/milestones/edit', methods=['POST'])
    def edit_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone'),
                                                        requests.put, request.form,
                                                        ['ID', 'RoadmapID', 'VersionCode', 'VersionName',
                                                         'Title', 'DueDate', 'CompletionDate', 'Status'])

        if not success:
            return response
        return redirect(url_for('admin_milestones.overview', roadmap_ID=request.args.get('roadmap_ID')))

    @milestones.route('/admin/milestones/delete', methods=['GET'])
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('milestone', ID), requests.delete, {}, [])
        if not success:
            return response
        return redirect(url_for('admin_milestones.overview', roadmap_ID=request.args.get('roadmap_ID')))

    return milestones

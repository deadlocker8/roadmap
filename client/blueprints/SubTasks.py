import requests
from flask import Blueprint, render_template, redirect, url_for, request

from AdminWrapper import require_api_token
from ApiRequest import ApiRequest
from Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    subtasks = Blueprint('admin_subtasks', __name__)

    @subtasks.route('/admin/subtasks/overview', methods=['GET'])
    @require_api_token
    def overview():
        task_ID = request.args.get('task_ID')
        if not task_ID or int(task_ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        task = requests.get(urlBuilder.build_url('task', task_ID)).json()
        subtasks = requests.get(urlBuilder.build_url('subtasks', task_ID)).json()
        return render_template('admin/subtasks/overview.html', subtasks=subtasks, task=task)

    @subtasks.route('/admin/subtasks/add', methods=['GET'])
    @require_api_token
    def add():
        return render_template('admin/subtasks/edit.html',
                               title='New SubTask',
                               task_ID=request.args.get('task_ID'),
                               form_url=url_for('admin_subtasks.add_post'))

    @subtasks.route('/admin/subtasks/add', methods=['POST'])
    @require_api_token
    def add_post():
        params = dict(request.form)
        params['Status'] = '1' if 'Status' in params else '0'

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('subtask'),
                                                        requests.post, params,
                                                        [('TaskID', int), ('Title', str), ('Description', str),
                                                         ('Status', int)])

        if not success:
            return response
        return redirect(url_for('admin_subtasks.overview', task_ID=request.form.get('TaskID')))

    @subtasks.route('/admin/subtasks/edit', methods=['GET'])
    @require_api_token
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        subtask = requests.get(urlBuilder.build_url('subtask', ID)).json()
        return render_template('admin/subtasks/edit.html',
                               title='Edit SubTask',
                               task_ID=request.args.get('task_ID'),
                               subtask=subtask,
                               form_url=url_for('admin_subtasks.edit_post'))

    @subtasks.route('/admin/subtasks/edit', methods=['POST'])
    @require_api_token
    def edit_post():
        params = dict(request.form)
        params['Status'] = '1' if 'Status' in params else '0'

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('subtask'),
                                                        requests.put, params,
                                                        [('ID', int), ('TaskID', int), ('Title', str),
                                                         ('Description', str), ('Status', int)])
        if not success:
            return response
        return redirect(url_for('admin_subtasks.overview', task_ID=params['TaskID']))

    @subtasks.route('/admin/subtasks/delete', methods=['GET'])
    @require_api_token
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('subtask', ID), requests.delete, {}, [])
        if not success:
            return response

        return redirect(url_for('admin_subtasks.overview', task_ID=request.args.get('task_ID')))

    return subtasks

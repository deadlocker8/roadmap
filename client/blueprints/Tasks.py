import requests
from flask import Blueprint, render_template, redirect, url_for, request

from AdminWrapper import require_api_token
from ApiRequest import ApiRequest
from Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    tasks = Blueprint('admin_tasks', __name__)

    @tasks.route('/admin/tasks/overview', methods=['GET'])
    @require_api_token
    def overview():
        milestone_ID = request.args.get('milestone_ID')
        if not milestone_ID or int(milestone_ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        milestone = requests.get(urlBuilder.build_url('milestone', milestone_ID)).json()
        tasks = requests.get(urlBuilder.build_url('tasks', milestone_ID)).json()
        return render_template('admin/tasks/overview.html', tasks=tasks, milestone=milestone)

    @tasks.route('/admin/tasks/add', methods=['GET'])
    @require_api_token
    def add():
        return render_template('admin/tasks/edit.html',
                               title='New Task',
                               milestone_ID=request.args.get('milestone_ID'),
                               form_url=url_for('admin_tasks.add_post'))

    @tasks.route('/admin/tasks/add', methods=['POST'])
    @require_api_token
    def add_post():
        params = dict(request.form)
        params['Status'] = '1' if 'Status' in params else '0'

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('task'),
                                                        requests.post, params,
                                                        ['MilestoneID', 'Title', 'Description', 'Status'])

        if not success:
            return response
        return redirect(url_for('admin_tasks.overview', milestone_ID=request.form.get('MilestoneID')))

    @tasks.route('/admin/tasks/edit', methods=['GET'])
    @require_api_token
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        task = requests.get(urlBuilder.build_url('task', ID)).json()
        return render_template('admin/tasks/edit.html',
                               title='Edit Task',
                               milestone_ID=request.args.get('milestone_ID'),
                               task=task,
                               form_url=url_for('admin_tasks.edit_post'))

    @tasks.route('/admin/tasks/edit', methods=['POST'])
    @require_api_token
    def edit_post():
        params = dict(request.form)
        params['Status'] = '1' if 'Status' in params else '0'

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('task'),
                                                        requests.put, params,
                                                        ['ID', 'MilestoneID', 'Title', 'Description', 'Status'])
        if not success:
            return response
        return redirect(url_for('admin_tasks.overview', milestone_ID=params['MilestoneID']))

    @tasks.route('/admin/tasks/delete', methods=['GET'])
    @require_api_token
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('task', ID), requests.delete, {}, [])
        if not success:
            return response

        return redirect(url_for('admin_tasks.overview', milestone_ID=request.args.get('milestone_ID')))

    return tasks

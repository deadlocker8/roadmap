import requests
from flask import Blueprint, render_template, redirect, url_for, request

from ApiRequest import ApiRequest
from Localization import LOCALIZATION


def construct_blueprint(urlBuilder):
    tasks = Blueprint('admin_tasks', __name__)

    @tasks.route('/admin/tasks/overview', methods=['GET'])
    def overview():
        milestone_ID = request.args.get('milestone_ID')
        if not milestone_ID or int(milestone_ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        milestone = requests.get(urlBuilder.build_url('milestone', milestone_ID)).json()
        tasks = requests.get(urlBuilder.build_url('tasks', milestone_ID)).json()
        return render_template('admin/tasks/overview.html', tasks=tasks, milestone=milestone)

    @tasks.route('/admin/tasks/add', methods=['GET'])
    def add():
        return render_template('admin/tasks/edit.html',
                               title='New Task',
                               roadmap_ID=request.args.get('roadmap_ID'),
                               form_url=url_for('admin_tasks.add_post'))

    @tasks.route('/admin/tasks/add', methods=['POST'])
    def add_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('task'),
                                                        requests.post, request.form,
                                                        ['MilestoneID', 'Title', 'Description', 'Status'])

        if not success:
            return response
        return redirect(url_for('admin_tasks.overview', roadmap_ID=request.form.get('MilestoneID')))

    @tasks.route('/admin/tasks/edit', methods=['GET'])
    def edit():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        task = requests.get(urlBuilder.build_url('milestone', ID)).json()
        return render_template('admin/tasks/edit.html',
                               title='Edit Task',
                               task=task,
                               form_url=url_for('admin_tasks.edit_post'))

    @tasks.route('/admin/tasks/edit', methods=['POST'])
    def edit_post():
        success, response = ApiRequest.send_api_request(urlBuilder.build_url('task'),
                                                        requests.put, request.form,
                                                        ['ID', 'MilestoneID', 'Title', 'Description', 'Status'])
        if not success:
            return response

        milestone = requests.get(urlBuilder.build_url('milestone', request.args['milestone_ID'])).json()
        return redirect(url_for('admin_tasks.overview', milestone=milestone))

    @tasks.route('/admin/tasks/delete', methods=['GET'])
    def delete():
        ID = request.args.get('ID')
        if not ID or int(ID) < 0:
            return render_template('error.html', message=LOCALIZATION['error_param_invalid'])

        success, response = ApiRequest.send_api_request(urlBuilder.build_url('task', ID), requests.delete, {}, [])
        if not success:
            return response

        return redirect(url_for('admin_tasks.overview', milestone_ID=request.args['milestone_ID']))

    return tasks

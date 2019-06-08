from flask import Blueprint, jsonify


def construct_blueprint(database):
    task_api = Blueprint('task_api', __name__)

    @task_api.route('/tasks/<int:milestoneID>', methods=['GET'])
    def get_tasks(milestoneID):
        return jsonify(database.get_tasks(milestoneID))

    @task_api.route('/tasks/<int:milestoneID>/open', methods=['GET'])
    def get_open_tasks(milestoneID):
        return jsonify(database.get_open_tasks(milestoneID))

    @task_api.route('/task/<int:taskID>', methods=['GET'])
    def get_task(taskID):
        return jsonify(database.get_task(taskID))

    return task_api

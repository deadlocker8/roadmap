from flask import Blueprint, jsonify


def construct_blueprint(database):
    subtask_api = Blueprint('subtask_api', __name__)

    @subtask_api.route('/subtasks/<int:taskID>', methods=['GET'])
    def get_sub_tasks(taskID):
        return jsonify(database.get_sub_tasks(taskID))

    @subtask_api.route('/subtasks/<int:taskID>/open', methods=['GET'])
    def get_open_sub_tasks(taskID):
        return jsonify(database.get_open_sub_tasks(taskID))

    @subtask_api.route('/subtask/<int:subTaskID>', methods=['GET'])
    def get_sub_task(subTaskID):
        return jsonify(database.get_sub_task(subTaskID))

    return subtask_api

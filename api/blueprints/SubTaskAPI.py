from enum import Enum

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from logic.RequestValidator import RequestValidator, ValidationError


class SubTaskParameters(Enum):
    ID = 'ID'
    TASK_ID = 'TaskID'
    TITLE = 'Title'
    DESCRIPTION = 'Description'
    STATUS = 'Status'

    @staticmethod
    def get_values():
        return [m.value for m in SubTaskParameters]


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

    @subtask_api.route('/subtask', methods=['POST'])
    @jwt_required
    def add_sub_task():
        try:
            parameters = RequestValidator.validate(request, [SubTaskParameters.TASK_ID.value,
                                                             SubTaskParameters.TITLE.value,
                                                             SubTaskParameters.DESCRIPTION.value,
                                                             SubTaskParameters.STATUS.value])
        except ValidationError as e:
            return e.response, 400

        database.add_sub_task(parameters[SubTaskParameters.TASK_ID.value],
                              parameters[SubTaskParameters.TITLE.value],
                              parameters[SubTaskParameters.DESCRIPTION.value],
                              parameters[SubTaskParameters.STATUS.value])
        return jsonify({'success': True})

    @subtask_api.route('/subtask/<int:subTaskID>', methods=['DELETE'])
    @jwt_required
    def delete_sub_task(subTaskID):
        if not __subtask_exists(subTaskID):
            return jsonify({'success': False, 'msg': "No sub task with id '{}' existing".format(subTaskID)}), 400

        database.delete_sub_task(subTaskID)
        return jsonify({'success': True})

    @subtask_api.route('/subtask', methods=['PUT'])
    @jwt_required
    def update_sub_task():
        try:
            parameters = RequestValidator.validate(request, SubTaskParameters.get_values())
        except ValidationError as e:
            return e.response, 400

        subtaskID = parameters[SubTaskParameters.ID.value]
        if not __subtask_exists(subtaskID):
            return jsonify({'success': False, 'msg': "No sub task with ID '{}' existing".format(subtaskID)}), 400

        database.update_sub_task(subtaskID,
                                 parameters[SubTaskParameters.TASK_ID.value],
                                 parameters[SubTaskParameters.TITLE.value],
                                 parameters[SubTaskParameters.DESCRIPTION.value],
                                 parameters[SubTaskParameters.STATUS.value])
        return jsonify({'success': True})

    def __subtask_exists(subtaskID):
        subtaskID = int(subtaskID)
        availableIDs = [jsonify(subtask).json[SubTaskParameters.ID.value] for subtask in database.get_all_sub_tasks()]
        return subtaskID in availableIDs

    return subtask_api

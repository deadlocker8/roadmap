from enum import Enum

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from RequestValidator import RequestValidator, ValidationError


class TaskParameters(Enum):
    ID = "ID"
    MILESTONE_ID = "MilestoneID"
    TITLE = "Title"
    DESCRIPTION = "Description"
    STATUS = "Status"

    @staticmethod
    def get_values():
        return [m.value for m in TaskParameters]


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

    @task_api.route('/task', methods=['POST'])
    @jwt_required
    def add_task():
        try:
            parameters = RequestValidator.validate(request, [TaskParameters.MILESTONE_ID.value,
                                                             TaskParameters.TITLE.value,
                                                             TaskParameters.DESCRIPTION.value])
        except ValidationError as e:
            return e.response, 400

        database.add_task(parameters[TaskParameters.MILESTONE_ID.value],
                          parameters[TaskParameters.TITLE.value],
                          parameters[TaskParameters.DESCRIPTION.value])
        return jsonify({"success": True})

    @task_api.route('/task', methods=['DELETE'])
    @jwt_required
    def delete_task():
        try:
            parameters = RequestValidator.validate(request, [TaskParameters.ID.value])
        except ValidationError as e:
            return e.response, 400

        taskID = parameters[TaskParameters.ID.value]
        if not __task_exists(taskID):
            return jsonify({"success": False, "msg": "No task with ID '{}' existing".format(taskID)}), 400

        database.delete_task(taskID)
        return jsonify({"success": True})

    @task_api.route('/task', methods=['PUT'])
    @jwt_required
    def update_task():
        try:
            parameters = RequestValidator.validate(request, TaskParameters.get_values())
        except ValidationError as e:
            return e.response, 400

        taskID = parameters[TaskParameters.ID.value]
        if not __task_exists(taskID):
            return jsonify({"success": False, "msg": "No task with ID '{}' existing".format(taskID)}), 400

        database.update_task(taskID,
                             parameters[TaskParameters.MILESTONE_ID.value],
                             parameters[TaskParameters.TITLE.value],
                             parameters[TaskParameters.DESCRIPTION.value],
                             parameters[TaskParameters.STATUS.value])
        return jsonify({"success": True})

    def __task_exists(taskID):
        taskID = int(taskID)
        availableIDs = [jsonify(task).json[TaskParameters.ID.value] for task in database.get_all_tasks()]
        return taskID in availableIDs

    return task_api

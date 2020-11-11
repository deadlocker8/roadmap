from enum import Enum

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity

from logic.DateFormatter import DateFormatter
from logic.RequestValidator import RequestValidator, ValidationError


class RoadmapParameters(Enum):
    ID = 'ID'
    PROJECT_NAME = 'Projectname'
    HIDDEN = 'Hidden'


def construct_blueprint(database):
    roadmap_api = Blueprint('roadmap_api', __name__)

    @roadmap_api.route('/roadmaps', methods=['GET'])
    @jwt_optional
    def get_visible_roadmaps():
        user = get_jwt_identity()
        if user is not None:
            return jsonify(database.get_roadmaps())
        else:
            return jsonify(database.get_visible_roadmaps())

    @roadmap_api.route('/roadmap/<int:roadmapID>', methods=['GET'])
    @jwt_optional
    def get_roadmap(roadmapID):
        roadmap = database.get_roadmap(roadmapID)

        user = get_jwt_identity()
        if roadmap['Hidden'] and user is None:
                return jsonify({'success': False, 'msg': 'A roadmap with this id not exists'}), 404
        return jsonify(roadmap)

    @roadmap_api.route('/roadmap/<int:roadmapID>/full', methods=['GET'])
    @jwt_optional
    def get_roadmap_full(roadmapID):
        roadmap = database.get_roadmap(roadmapID)
        roadmap['milestones'] = database.get_milestones(roadmapID)

        user = get_jwt_identity()
        if roadmap['Hidden'] and user is None:
            return jsonify({'success': False, 'msg': 'A roadmap with this id not exists'}), 404

        numberOfOpenMilestones = 0
        for milestone in roadmap['milestones']:
            milestone['DueDate'] = DateFormatter.format(milestone['DueDate'])
            milestone['CompletionDate'] = DateFormatter.format(milestone['CompletionDate'])

            if milestone['Status'] == 0:
                numberOfOpenMilestones += 1

            milestone['tasks'] = database.get_tasks(milestone[RoadmapParameters.ID.value])

            numberOfOpenTasks = 0
            for task in milestone['tasks']:
                task['subtasks'] = database.get_sub_tasks(task[RoadmapParameters.ID.value])

                numberOfOpenSubTasks = 0
                for subtask in task['subtasks']:
                    if subtask['Status'] == 0:
                        numberOfOpenSubTasks += 1
                task['numberOfOpenSubTasks'] = numberOfOpenSubTasks

                if task['Status'] == 0:
                    numberOfOpenTasks += 1
            milestone['numberOfOpenTasks'] = numberOfOpenTasks

        roadmap['numberOfOpenMilestones'] = numberOfOpenMilestones
        return jsonify(roadmap)

    @roadmap_api.route('/roadmap', methods=['POST'])
    @jwt_required
    def add_roadmap():
        try:
            parameters = RequestValidator.validate(request, [RoadmapParameters.PROJECT_NAME.value])
        except ValidationError as e:
            return e.response, 400

        if __name_already_used(parameters[RoadmapParameters.PROJECT_NAME.value]):
            return jsonify({'success': False, 'msg': 'A roadmap with this name already exists'}), 400

        database.add_roadmap(parameters[RoadmapParameters.PROJECT_NAME.value])
        return jsonify({'success': True})

    @roadmap_api.route('/roadmap/<int:roadmapID>', methods=['DELETE'])
    @jwt_required
    def delete_roadmap(roadmapID):
        if not __roadmaps_exists(roadmapID):
            return jsonify({'success': False, 'msg': "No roadmap with id '{}' existing".format(roadmapID)}), 400

        database.delete_roadmap(roadmapID)
        return jsonify({'success': True})

    @roadmap_api.route('/roadmap', methods=['PUT'])
    @jwt_required
    def update_roadmap():
        try:
            parameters = RequestValidator.validate(request, [
                RoadmapParameters.ID.value,
                RoadmapParameters.PROJECT_NAME.value,
                RoadmapParameters.HIDDEN.value
            ])
        except ValidationError as e:
            return e.response, 400

        roadmapID = parameters[RoadmapParameters.ID.value]
        if not __roadmaps_exists(roadmapID):
            return jsonify({'success': False, 'msg': "No roadmap with ID '{}' existing".format(roadmapID)}), 400

        database.update_roadmap(parameters[RoadmapParameters.ID.value],
                                parameters[RoadmapParameters.PROJECT_NAME.value],
                                parameters[RoadmapParameters.HIDDEN.value])
        return jsonify({'success': True})

    def __roadmaps_exists(roadmapID):
        roadmapID = int(roadmapID)
        availableIDs = [jsonify(roadmap).json[RoadmapParameters.ID.value] for roadmap in database.get_roadmaps()]
        return roadmapID in availableIDs

    def __name_already_used(name):
        usedNames = [jsonify(roadmap).json[RoadmapParameters.PROJECT_NAME.value] for roadmap in database.get_roadmaps()]
        return name in usedNames

    return roadmap_api

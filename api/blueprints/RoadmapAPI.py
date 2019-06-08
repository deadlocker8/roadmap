from datetime import datetime
from enum import Enum

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from RequestValidator import RequestValidator, ValidationError

DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)


class RoadmapParameters(Enum):
    ID = "ID"
    PROJECT_NAME = "Projectname"


def construct_blueprint(database):
    roadmap_api = Blueprint('roadmap_api', __name__)

    @roadmap_api.route('/roadmaps', methods=['GET'])
    def get_roadmaps():
        return jsonify(database.get_roadmaps())

    @roadmap_api.route('/roadmap/<int:roadmapID>', methods=['GET'])
    def get_roadmap(roadmapID):
        return jsonify(database.get_roadmap(roadmapID))

    @roadmap_api.route('/roadmap/<int:roadmapID>/full', methods=['GET'])
    def get_roadmap_fast(roadmapID):
        roadmap = database.get_roadmap(roadmapID)
        roadmap["milestones"] = database.get_milestones(roadmapID)

        numberOfOpenMilestones = 0
        for milestone in roadmap["milestones"]:
            if milestone["DueDate"] == DEFAULT_DATE:
                milestone["DueDate"] = "-"
            else:
                milestone["DueDate"] = datetime.strftime(milestone["DueDate"], "%d.%m.%Y")

            if milestone["CompletionDate"] == DEFAULT_DATE:
                milestone["CompletionDate"] = "-"
            else:
                milestone["CompletionDate"] = datetime.strftime(milestone["CompletionDate"], "%d.%m.%Y")

            if milestone["Status"] == 0:
                numberOfOpenMilestones += 1

            milestone["tasks"] = database.get_tasks(milestone[RoadmapParameters.ID])

            numberOfOpenTasks = 0
            for task in milestone["tasks"]:
                task["subtasks"] = database.get_sub_tasks(task[RoadmapParameters.ID])

                numberOfOpenSubTasks = 0
                for subtask in task["subtasks"]:
                    if subtask["Status"] == 0:
                        numberOfOpenSubTasks += 1
                task["numberOfOpenSubTasks"] = numberOfOpenSubTasks

                if task["Status"] == 0:
                    numberOfOpenTasks += 1
            milestone["numberOfOpenTasks"] = numberOfOpenTasks

        roadmap["numberOfOpenMilestones"] = numberOfOpenMilestones
        return jsonify(roadmap)

    @roadmap_api.route('/roadmap', methods=['POST'])
    @jwt_required
    def add_roadmap():
        try:
            parameters = RequestValidator.validate(request, [RoadmapParameters.PROJECT_NAME])
        except ValidationError as e:
            return e.response, 400

        if __name_already_used(parameters[RoadmapParameters.PROJECT_NAME]):
            return jsonify({"success": False, "msg": "A roadmap with this name already exists"}), 400

        database.add_roadmap(parameters[RoadmapParameters.PROJECT_NAME])
        return jsonify({"success": True})

    @roadmap_api.route('/roadmap/<int:roadmapID>', methods=['DELETE'])
    @jwt_required
    def delete_roadmap(roadmapID):
        if not __roadmaps_exists(roadmapID):
            return jsonify({"success": False, "msg": "No roadmap with id '{}' existing".format(roadmapID)}), 400

        database.delete_roadmap(roadmapID)
        return jsonify({"success": True})

    @roadmap_api.route('/roadmap', methods=['PUT'])
    @jwt_required
    def update_roadmap():
        try:
            parameters = RequestValidator.validate(request, [RoadmapParameters.ID, RoadmapParameters.PROJECT_NAME])
        except ValidationError as e:
            return e.response, 400

        roadmapID = parameters[RoadmapParameters.ID]
        if not __roadmaps_exists(roadmapID):
            return jsonify({"success": False, "msg": "No roadmap with ID '{}' existing".format(roadmapID)}), 400

        if __name_already_used(parameters[RoadmapParameters.PROJECT_NAME]):
            return jsonify({"success": False, "msg": "A roadmap with this name already exists"}), 400

        database.update_roadmap(parameters[RoadmapParameters.ID], parameters[RoadmapParameters.PROJECT_NAME])
        return jsonify({"success": True})

    def __roadmaps_exists(roadmapID):
        roadmapID = int(roadmapID)
        availableIDs = [jsonify(roadmap).json[RoadmapParameters.ID] for roadmap in database.get_roadmaps()]
        return roadmapID in availableIDs

    def __name_already_used(name):
        usedNames = [jsonify(roadmap).json[RoadmapParameters.Projectname] for roadmap in database.get_roadmaps()]
        return name in usedNames

    return roadmap_api
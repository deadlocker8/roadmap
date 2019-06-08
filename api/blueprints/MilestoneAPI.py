from enum import Enum

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from RequestValidator import RequestValidator, ValidationError


class MilestoneParameters(Enum):
    ID = "ID"
    ROADMAP_ID = "RoadmapID"
    VERSION_CODE = "VersionCode"
    VERSION_NAME = "VersionName"
    TITLE = "Title"
    DUE_DATE = "DueDate"
    COMPLETION_DATE = "CompletionDate"
    STATUS = "Status"

    @staticmethod
    def get_values():
        return [m.value for m in MilestoneParameters]


def construct_blueprint(database):
    milestone_api = Blueprint('milestone_api', __name__)

    @milestone_api.route('/milestones/<int:roadmapID>', methods=['GET'])
    def get_milestones(roadmapID):
        return jsonify(database.get_milestones(roadmapID))

    @milestone_api.route('/milestones/<int:roadmapID>/open', methods=['GET'])
    def get_open_milestones(roadmapID):
        return jsonify(database.get_open_milestones(roadmapID))

    @milestone_api.route('/milestones/<int:roadmapID>/latest', methods=['GET'])
    def get_latest_milestone(roadmapID):
        return jsonify(database.get_latest_milestone(roadmapID))

    @milestone_api.route('/milestone/<int:milestoneID>', methods=['GET'])
    def get_milestone(milestoneID):
        return jsonify(database.get_milestone(milestoneID))

    @milestone_api.route('/milestone', methods=['POST'])
    @jwt_required
    def add_milestone():
        try:
            parameters = RequestValidator.validate(request, [MilestoneParameters.ROADMAP_ID.value,
                                                             MilestoneParameters.VERSION_CODE.value,
                                                             MilestoneParameters.VERSION_NAME.value,
                                                             MilestoneParameters.TITLE.value,
                                                             MilestoneParameters.DUE_DATE.value,
                                                             MilestoneParameters.COMPLETION_DATE.value])
        except ValidationError as e:
            return e.response, 400

        database.add_milestone(parameters[MilestoneParameters.ROADMAP_ID.value],
                               parameters[MilestoneParameters.VERSION_CODE.value],
                               parameters[MilestoneParameters.VERSION_NAME.value],
                               parameters[MilestoneParameters.TITLE.value],
                               parameters[MilestoneParameters.DUE_DATE.value],
                               parameters[MilestoneParameters.COMPLETION_DATE.value])
        return jsonify({"success": True})

    @milestone_api.route('/milestone', methods=['DELETE'])
    @jwt_required
    def delete_milestone():
        try:
            parameters = RequestValidator.validate(request, [MilestoneParameters.ID.value])
        except ValidationError as e:
            return e.response, 400

        milestoneID = parameters[MilestoneParameters.ID.value]
        if not __milestone_exists(milestoneID):
            return jsonify({"success": False, "msg": "No milestone with ID '{}' existing".format(milestoneID)}), 400

        database.delete_roadmap(milestoneID)
        return jsonify({"success": True})

    @milestone_api.route('/milestone', methods=['PUT'])
    @jwt_required
    def update_milestone():
        try:
            parameters = RequestValidator.validate(request, MilestoneParameters.get_values())
        except ValidationError as e:
            return e.response, 400

        milestoneID = parameters[MilestoneParameters.ID.value]
        if not __milestone_exists(milestoneID):
            return jsonify({"success": False, "msg": "No milestone with ID '{}' existing".format(milestoneID)}), 400

        database.update_milestone(milestoneID,
                                  parameters[MilestoneParameters.ROADMAP_ID.value],
                                  parameters[MilestoneParameters.VERSION_CODE.value],
                                  parameters[MilestoneParameters.VERSION_NAME.value],
                                  parameters[MilestoneParameters.TITLE.value],
                                  parameters[MilestoneParameters.DUE_DATE.value],
                                  parameters[MilestoneParameters.COMPLETION_DATE.value],
                                  parameters[MilestoneParameters.STATUS.value])
        return jsonify({"success": True})

    def __milestone_exists(milestoneID):
        milestoneID = int(milestoneID)
        availableIDs = [jsonify(milestone).json[MilestoneParameters.ID.value] for milestone in
                        database.get_all_milestones()]
        return milestoneID in availableIDs

    return milestone_api

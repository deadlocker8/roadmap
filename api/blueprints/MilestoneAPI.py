from enum import Enum

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from DateFormatter import DateFormatter
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


def format_milestones(milestones):
    result = []
    for milestone in milestones:
        result.append(prepare_milestone(milestone))
    return result


def prepare_milestone(milestone):
    milestone[MilestoneParameters.DUE_DATE.value] = DateFormatter.format(
        milestone[MilestoneParameters.DUE_DATE.value])
    milestone[MilestoneParameters.COMPLETION_DATE.value] = DateFormatter.format(
        milestone[MilestoneParameters.COMPLETION_DATE.value])
    return milestone


def construct_blueprint(database):
    milestone_api = Blueprint('milestone_api', __name__)

    @milestone_api.route('/milestones/<int:roadmapID>', methods=['GET'])
    def get_milestones(roadmapID):
        milestones = database.get_milestones(roadmapID)
        return jsonify(format_milestones(milestones))

    @milestone_api.route('/milestones/<int:roadmapID>/open', methods=['GET'])
    def get_open_milestones(roadmapID):
        milestones = database.get_open_milestones(roadmapID)
        return jsonify(format_milestones(milestones))

    @milestone_api.route('/milestones/<int:roadmapID>/latest', methods=['GET'])
    def get_latest_milestone(roadmapID):
        milestones = database.get_latest_milestone(roadmapID)
        return jsonify(format_milestones(milestones))

    @milestone_api.route('/milestone/<int:milestoneID>', methods=['GET'])
    def get_milestone(milestoneID):
        milestone = database.get_milestone(milestoneID)
        return jsonify(prepare_milestone(milestone))

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
                               parameters[MilestoneParameters.COMPLETION_DATE.value],
                               parameters[MilestoneParameters.STSTUS.value])
        return jsonify({"success": True})

    @milestone_api.route('/milestone/<int:milestoneID>', methods=['DELETE'])
    @jwt_required
    def delete_milestone(milestoneID):
        if not __milestone_exists(milestoneID):
            return jsonify({"success": False, "msg": "No milestone with id '{}' existing".format(milestoneID)}), 400

        database.delete_milestone(milestoneID)
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

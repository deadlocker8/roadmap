from flask import Blueprint, jsonify


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

    return milestone_api

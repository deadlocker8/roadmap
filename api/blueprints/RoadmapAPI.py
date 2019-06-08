from datetime import datetime

from flask import Blueprint, jsonify, request

from RequestValidator import RequestValidator, ValidationError

DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)


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

            milestone["tasks"] = database.get_tasks(milestone["ID"])

            numberOfOpenTasks = 0
            for task in milestone["tasks"]:
                task["subtasks"] = database.get_sub_tasks(task["ID"])

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
    def add_roadmap():
        try:
            parameters = RequestValidator.validate(request, ["name"])
        except ValidationError as e:
            return e.response, 400

        if __name_already_used(parameters["name"]):
            return jsonify({"success": False, "message": "A roadmap with this name already exists"}), 400

        database.add_roadmap(parameters["name"])
        return jsonify({"success": True})

    @roadmap_api.route('/roadmap', methods=['DELETE'])
    def delete_roadmap():
        try:
            parameters = RequestValidator.validate(request, ["id"])
        except ValidationError as e:
            return e.response, 400

        roadmapID = parameters["id"]
        if not __roadmaps_exists(roadmapID):
            return jsonify({"success": False, "message": "No roadmap with id '{}' existing".format(roadmapID)}), 400

        database.delete_roadmap(roadmapID)
        return jsonify({"success": True})

    @roadmap_api.route('/roadmap', methods=['PUT'])
    def update_roadmap():
        try:
            parameters = RequestValidator.validate(request, ["id", "name"])
        except ValidationError as e:
            return e.response, 400

        roadmapID = parameters["id"]
        if not __roadmaps_exists(roadmapID):
            return jsonify({"success": False, "message": "No roadmap with id '{}' existing".format(roadmapID)}), 400

        if __name_already_used(parameters["name"]):
            return jsonify({"success": False, "message": "A roadmap with this name already exists"}), 400

        database.update_roadmap(parameters["id"], parameters["name"])
        return jsonify({"success": True})

    def __roadmaps_exists(roadmapID):
        roadmapID = int(roadmapID)
        availableIDs = [jsonify(roadmap).json["ID"] for roadmap in database.get_roadmaps()]
        return roadmapID in availableIDs

    def __name_already_used(name):
        usedNames = [jsonify(roadmap).json["Projectname"] for roadmap in database.get_roadmaps()]
        return name in usedNames

    return roadmap_api

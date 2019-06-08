from datetime import datetime

from flask import Blueprint, jsonify

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

    return roadmap_api

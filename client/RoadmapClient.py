from datetime import datetime

import requests
from flask import Flask, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

API_URL = "http://127.0.0.1:5000"
DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)
LOCALIZATION = {"due_by": "Due by",
                "done": "Done",
                "done_at": "Done at"}


def build_url(*parts):
    part = '/'.join(str(x) for x in parts)
    return "{}/{}".format(API_URL, part)


@app.route("/")
def overview():
    roadmaps = requests.get(build_url("roadmaps")).json()
    return render_template("overview.html", roadmaps=roadmaps)


@app.route("/roadmap/<roadmapID>")
def roadmap(roadmapID):
    try:
        roadmapID = int(roadmapID)
    except ValueError:
        return "Invalid roadmap ID"

    if roadmapID < 1:
        return "Invalid roadmap ID"

    roadmap = requests.get(build_url("roadmap", roadmapID)).json()
    roadmap["milestones"] = requests.get(build_url("milestones", roadmapID)).json()

    numberOfOpenMilestones = 0
    for milestone in roadmap["milestones"]:
        dueDate = datetime.strptime(milestone["DueDate"], "%a, %d %b %Y %H:%M:%S %Z")
        if dueDate == DEFAULT_DATE:
            milestone["DueDate"] = "-"
        else:
            milestone["DueDate"] = datetime.strftime(dueDate, "%d.%m.%Y")

        completionDate = datetime.strptime(milestone["CompletionDate"], "%a, %d %b %Y %H:%M:%S %Z")
        if completionDate == DEFAULT_DATE:
            milestone["CompletionDate"] = "-"
        else:
            milestone["CompletionDate"] = datetime.strftime(completionDate, "%d.%m.%Y")

        if milestone["Status"] == 0:
            numberOfOpenMilestones += 1

        milestone["tasks"] = requests.get(build_url("tasks", milestone["ID"])).json()

        numberOfOpenTasks = 0
        for task in milestone["tasks"]:
            task["subtasks"] = requests.get(build_url("subtasks", task["ID"])).json()

            numberOfOpenSubTasks = 0
            for subtask in task["subtasks"]:
                if subtask["Status"] == 0:
                    numberOfOpenSubTasks += 1
            task["numberOfOpenSubTasks"] = numberOfOpenSubTasks

            if task["Status"] == 0:
                numberOfOpenTasks += 1
        milestone["numberOfOpenTasks"] = numberOfOpenTasks

    roadmap["numberOfOpenMilestones"] = numberOfOpenMilestones

    return render_template("index.html", roadmap=roadmap, localization=LOCALIZATION)


if __name__ == "__main__":
    http_server = WSGIServer(("0.0.0.0", 10000), app)
    http_server.serve_forever()

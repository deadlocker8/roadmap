import json
from datetime import datetime

import requests
from flask import Flask, render_template, redirect
from gevent.pywsgi import WSGIServer

from Localization import LOCALIZATION

app = Flask(__name__)

with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

DEFAULT_DATE = datetime(2000, 1, 1, 0, 0, 0)


def build_url(*parts):
    part = '/'.join(str(x) for x in parts)
    return "{}/{}".format(SETTINGS["apiURL"], part)


@app.route("/")
def overview():
    roadmaps = requests.get(build_url("roadmaps")).json()
    return render_template("overview.html", roadmaps=roadmaps)


@app.route("/roadmap/")
def roadmap():
    return redirect("/")


@app.route("/roadmap/<roadmapID>")
def roadmap_by_id(roadmapID):
    try:
        roadmapID = int(roadmapID)
    except ValueError:
        return render_template("error.html", message=LOCALIZATION["error_param_invalid"])

    if roadmapID < 1:
        return render_template("error.html", message=LOCALIZATION["error_param_invalid"])

    roadmap = requests.get(build_url("roadmap", roadmapID, "full")).json()
    if roadmap is None:
        return render_template("error.html", message=LOCALIZATION["error_roadmap_not_existing"])

    return render_template("index.html", roadmap=roadmap, localization=LOCALIZATION)


@app.route("/roadmap/<roadmapID>/fragment")
def roadmap_fragement_by_id(roadmapID):
    try:
        roadmapID = int(roadmapID)
    except ValueError:
        return render_template("error.html", message=LOCALIZATION["error_param_invalid"])

    if roadmapID < 1:
        return render_template("error.html", message=LOCALIZATION["error_param_invalid"])

    roadmap = requests.get(build_url("roadmap", roadmapID, "full")).json()
    if roadmap is None:
        return render_template("error.html", message=LOCALIZATION["error_roadmap_not_existing"])

    return render_template("roadmapFragment.html", roadmap=roadmap, localization=LOCALIZATION)


@app.route("/admin/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    if SETTINGS["useSSL"]:
        http_server = WSGIServer((SETTINGS["listen"],
                                  SETTINGS["port"]), app,
                                 keyfile=SETTINGS["keyfile"],
                                 certfile=SETTINGS["certfile"])
    else:
        http_server = WSGIServer((SETTINGS["listen"], SETTINGS["port"]), app)

    http_server.serve_forever()

from flask import Blueprint, render_template, redirect, send_from_directory
from flask import current_app as app

from pathlib import Path

from core import api

from plugins.learn.models import learn

pluginPages = Blueprint('learnPages', __name__, template_folder="templates")

@pluginPages.route('/learn/includes/<file>')
def custom_static(file):
    return send_from_directory(str(Path("plugins/learn/web/includes")), file)

@pluginPages.route("/learn/graph/<graphName>/",methods=["GET"])
def mainPage(graphName):
    graph = learn._learnGraph().getAsClass(sessionData=api.g.sessionData,query={ "name" : graphName })
    if len(graph) == 1:
        graph = graph[0]
        xy = graph.getGraph()
        return render_template("learnModel.html", x=xy[0], y=xy[1])
    return { "result" : "Not found" }, 404

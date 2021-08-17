from flask import Blueprint, render_template, redirect, send_from_directory
from flask import current_app as app

from pathlib import Path

from core import api

from plugins.learn.models import learn

pluginPages = Blueprint('learnPages', __name__, template_folder="templates")

@pluginPages.route('/includes/<file>')
def custom_static(file):
    return send_from_directory(str(Path("plugins/learn/web/includes")), file)

@pluginPages.route("/graph/<graphName>/",methods=["GET"])
def graphPage(graphName):
    graph = learn._learnGraph().getAsClass(sessionData=api.g.sessionData,query={ "name" : graphName })
    if len(graph) == 1:
        graph = graph[0]
        x,y = graph.getGraph()
        tempX = []
        tempY = []
        xyData = graph.getStatistics()
        for index in range(0,len(x)-1):
            if y[index] > xyData[str(x[index])]["mean"]-xyData[str(x[index])]["std"] and y[index] < xyData[str(x[index])]["mean"]+xyData[str(x[index])]["std"]:
                tempX.append(x[index])
                tempY.append(y[index])
        x = tempX
        y = tempY
        return render_template("learnModel.html", x=x, y=y, r2=graph.r2 )
    return { "result" : "Not found" }, 404

@pluginPages.route("/",methods=["GET"])
def mainPage():
    learnData = learn._learnGraph().query(sessionData=api.g.sessionData,query={})["results"]
    return render_template("learn.html", learnData=learnData )


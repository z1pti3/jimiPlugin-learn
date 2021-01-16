import numpy
import requests
from pathlib import Path
from sklearn.metrics import r2_score

from plugins.learn.models import learn
from core.models import action
from core import helpers, cache

class _learnPlotGraph(action._action):
	graphName = str()
	xy = str()

	def __init__(self):
		cache.globalCache.newCache("learnGraphCache")

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		xy = helpers.evalString(self.xy,{"data" : data})
		graph = cache.globalCache.get("learnGraphCache",graphName,getGraph)
		if graph != None and len(graph) > 0:
			graph = graph[0]
		else:
			learn._learnGraph().new(graphName,self.acl)
			graph = cache.globalCache.get("learnGraphCache",graphName,getGraph,forceUpdate=True)[0]
		
		graph.appendGraph(xy)

		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult

class _learnBuildPolynomialRegressionModel(action._action):
	graphName = str()
	stdMeanMode = bool()

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		graph = cache.globalCache.get("learnGraphCache",graphName,getGraph)
		if graph != None and len(graph) > 0:
			graph = graph[0]
			x,y = graph.getGraph()
			if self.stdMeanMode:
				tempX = []
				tempY = []
				xyData = graph.getStatistics()
				for index in range(0,len(x)-1):
					if y[index] > xyData[x[index]]["mean"]-xyData[x[index]]["std"] and y[index] < xyData[x[index]]["mean"]+xyData[x[index]]["std"]
						tempX.append(x[index])
						tempY.append(y[index])
				x = tempX
				y = tempY
			myModel = numpy.poly1d(numpy.polyfit(x, y, 10))
			r2 = r2_score(y, myModel(x))
			graph.saveModel(myModel,r2)

		actionResult["r2"] = r2
		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult

class _learnCalculateGraphStatistics(action._action):
	graphName = str()
	percentile = 90

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		graph = cache.globalCache.get("learnGraphCache",graphName,getGraph)
		actionResult["result"] = False
		actionResult["rc"] = 5
		if graph != None and len(graph) > 0:
			graph = graph[0]
			xArray,yArray = graph.getGraph()
			xyData = {}
			for index in range(0,len(xArray)-1):
				try:
					xyData[xArray[index]]["y"].append(yArray[index])
				except KeyError:
					xyData[xArray[index]] = { "y": [yArray[index]] }
			for x,value in xyData.items():
				xyData[x]["mean"] = numpy.mean(value["y"])
				xyData[x]["std"] = numpy.std(value["y"])
				xyData[x]["percentile"] = numpy.percentile(value["y"],self.percentile)
				del xyData[x]["y"]
			graph.setStatistics(xyData)
			actionResult["result"] = True
			actionResult["rc"] = 0
			actionResult["statistics"] = xyData
		return actionResult

class _learnGetGraphStatistics(action._action):
	graphName = str()

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		graph = cache.globalCache.get("learnGraphCache",graphName,getGraph)
		actionResult["result"] = False
		actionResult["rc"] = 404
		if graph != None and len(graph) > 0:
			graph = graph[0]
			xyData = graph.getStatistics()
			actionResult["result"] = True
			actionResult["rc"] = 0
			actionResult["statistics"] = xyData
		return actionResult

class _learnGraphPredict(action._action):
	graphName = str()
	value = str()

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		value = helpers.typeCast(helpers.evalString(self.value,{"data" : data}))
		graph = cache.globalCache.get("learnGraphCache",graphName,getGraph)
		if graph != None and len(graph) > 0:
			graph = graph[0]
			myModel = graph.getModel()
			actionResult["prediction"] = myModel(value)

		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult

class _learnGraphClean(action._action):
	graphName = str()
	preserveAmount = int()

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		graph = cache.globalCache.get("learnGraphCache",graphName,getGraph)
		if graph != None and len(graph) > 0:
			graph = graph[0]
			myModel = graph.cleanGraph(self.preserveAmount)
		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult

numpy.warnings.filterwarnings('ignore')

def getGraph(graphName,sessionData):
	return learn._learnGraph().getAsClass(query={ "name" : graphName },fields=["name","classID","_id","acl"]) 


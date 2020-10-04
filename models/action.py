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

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		graph = cache.globalCache.get("learnGraphCache",graphName,getGraph)
		if graph != None and len(graph) > 0:
			graph = graph[0]
			x,y = graph.getGraph()
			myModel = numpy.poly1d(numpy.polyfit(x, y, 10))
			r2 = r2_score(y, myModel(x))
			graph.saveModel(myModel,r2)

		actionResult["result"] = True
		actionResult["rc"] = 0
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


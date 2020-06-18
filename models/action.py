import requests
from pathlib import Path

from plugins.learn.models import learn
from core.models import action
from core import helpers, cache

class _learnPlotGraph(action._action):
	graphName = str()
	xy = list()

	def __init__(self):
		cache.globalCache.newCache("learnGraphCache")

	def run(self,data,persistentData,actionResult):
		graphName = helpers.evalString(self.graphName,{"data" : data})
		xy = helpers.evalList(self.xy,{"data" : data})
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



def getGraph(graphName,sessionData):
	return learn._learnGraph().getAsClass(query={ "name" : graphName },fields=["name","classID","_id","acl"]) 


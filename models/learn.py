import pickle
import time
from bson.binary import Binary

from core import db, helpers, logging

class _learnGraph(db._document):
    name = str()
    r2 = float()

    _dbCollection = db.db["learnGraph"]

    def new(self, name, acl):
        self.name = name
        self.acl = acl
        return super(_learnGraph, self).new()

    def appendGraph(self,xy):
        db.updateDocumentByID(self._dbCollection,self._id,{ "$push" : { "xy" : { "$each" : xy } }, "$set" : { "lastUpdateTime" : time.time() } })

    def getGraph(self):
        query = { "_id" : db.ObjectId(self._id) }
        doc = self._dbCollection.find_one(query)
        x = []
        y = []
        for xy in doc["xy"]:
            x.append(xy[0])
            y.append(xy[1])
        return (x,y)

    def saveModel(self,model,r2):
        # Check how safe this function is
        obj = pickle.dumps(model)
        db.updateDocumentByID(self._dbCollection,self._id,{ "$set" : { "model" : Binary(obj), "r2" : r2 } })

    def getModel(self):
        query = { "_id" : db.ObjectId(self._id) }
        doc = self._dbCollection.find_one(query)
        # Check how safe this function is
        return pickle.loads(doc["model"])
    

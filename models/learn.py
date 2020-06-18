import time

from core import db, helpers, logging

class _learnGraph(db._document):
    name = str()

    _dbCollection = db.db["learnGraph"]

    def new(self, name, acl):
        self.name = name
        self.acl = acl
        return super(_learnGraph, self).new()

    def appendGraph(self,xy):
        db.updateDocumentByID(self._dbCollection,self._id,{ "$push" : { "xy" : { "$each" : xy } }, "$set" : { "lastUpdateTime" : time.time() } })

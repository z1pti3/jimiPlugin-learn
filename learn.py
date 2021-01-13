from core import plugin, model

class _learn(plugin._plugin):
    version = 0.6

    def install(self):
        # Register models
        model.registerModel("learnGraph","_learnGraph","_document","plugins.learn.models.learn",True)
        model.registerModel("learnPlotGraph","_learnPlotGraph","_action","plugins.learn.models.action")
        model.registerModel("learnBuildPolynomialRegressionModel","_learnBuildPolynomialRegressionModel","_action","plugins.learn.models.action")
        model.registerModel("learnGraphPredict","_learnGraphPredict","_action","plugins.learn.models.action")
        model.registerModel("learnGraphClean","_learnGraphClean","_action","plugins.learn.models.action")
        model.registerModel("learnCalculateGraphStatistics","_learnCalculateGraphStatistics","_action","plugins.learn.models.action")
        model.registerModel("learnGetGraphStatistics","_learnGetGraphStatistics","_action","plugins.learn.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("learnGraph","_learnGraph","_document","plugins.learn.models.learn")
        model.deregisterModel("learnPlotGraph","_learnPlotGraph","_action","plugins.learn.models.action")
        model.deregisterModel("learnBuildPolynomialRegressionModel","_learnBuildPolynomialRegressionModel","_action","plugins.learn.models.action")
        model.deregisterModel("learnGraphPredict","_learnGraphPredict","_action","plugins.learn.models.action")
        model.deregisterModel("learnGraphClean","_learnGraphClean","_action","plugins.learn.models.action")
        model.deregisterModel("learnCalculateGraphStatistics","_learnCalculateGraphStatistics","_action","plugins.learn.models.action")
        model.registerModel("learnGetGraphStatistics","_learnGetGraphStatistics","_action","plugins.learn.models.action")
        return True

        
    def upgrade(self,LatestPluginVersion):
        if self.version < 0.6:
            model.registerModel("learnCalculateGraphStatistics","_learnCalculateGraphStatistics","_action","plugins.learn.models.action")
            model.registerModel("learnGetGraphStatistics","_learnGetGraphStatistics","_action","plugins.learn.models.action")
        if self.version < 0.5:
            model.registerModel("learnGraphClean","_learnGraphClean","_action","plugins.learn.models.action")
        if self.version < 0.4:
            model.registerModel("learnGraphPredict","_learnGraphPredict","_action","plugins.learn.models.action")
        if self.version < 0.3:
            model.registerModel("learnBuildPolynomialRegressionModel","_learnBuildPolynomialRegressionModel","_action","plugins.learn.models.action")
        if self.version < 0.2:
            model.registerModel("learnGraph","_learnGraph","_document","plugins.learn.models.learn",True)

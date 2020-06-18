from core import plugin, model

class _learn(plugin._plugin):
    version = 0.2

    def install(self):
        # Register models
        model.registerModel("learnGraph","_learnGraph","_document","plugins.event.models.learn",True)
        model.registerModel("learnPlotGraph","_learnPlotGraph","_action","plugins.learn.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("learnGraph","_learnGraph","_document","plugins.event.models.learn")
        model.deregisterModel("learnPlotGraph","_learnPlotGraph","_action","plugins.learn.models.action")
        return True

        
    def upgrade(self,LatestPluginVersion):
        if self.version < 0.2:
            model.registerModel("learnGraph","_learnGraph","_document","plugins.event.models.learn",True)
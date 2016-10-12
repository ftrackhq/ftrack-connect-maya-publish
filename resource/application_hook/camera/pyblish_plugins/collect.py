import pyblish.api
import ftrack_connect_pipeline.util


class FtrackPublishCollector(pyblish.api.ContextPlugin):
    '''Prepare ftrack publish.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add ftrack entity.'''
        ftrack_entity = ftrack_connect_pipeline.util.get_ftrack_entity()
        context.data['ftrack_entity'] = ftrack_entity


class CollectCameras(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        import maya.cmds as mc

        for grp in mc.ls(assemblies=True, long=True):
            if mc.ls(grp, dag=True, type="camera"):
                for family in ['ftrack.maya.mayabinary', 'ftrack.maya.alembic']:
                    instance = context.create_instance(
                        grp, family=family
                    )
                    instance.data['publish'] = True
                    instance.data['ftrack_components'] = []


pyblish.api.register_plugin(FtrackPublishCollector)
pyblish.api.register_plugin(CollectCameras)

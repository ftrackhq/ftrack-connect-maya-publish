# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import pyblish.api
import ftrack_connect_pipeline.util


class FtrackPublishCollector(pyblish.api.ContextPlugin):
    '''Prepare ftrack publish.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add ftrack entity.'''
        ftrack_entity = ftrack_connect_pipeline.util.get_ftrack_entity()
        context.data['ftrack_entity'] = ftrack_entity


class CollectGeometries(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya mesh instances.'''
        import maya.cmds as mc

        for grp in mc.ls(assemblies=True, long=True):
            if mc.ls(grp, dag=True, type="mesh"):
                instance = context.create_instance(
                    grp, family='ftrack.maya.geometry'
                )
                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(FtrackPublishCollector)
pyblish.api.register_plugin(CollectGeometries)

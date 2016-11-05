# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import pyblish.api
import ftrack_connect_pipeline.util


class CollectCameras(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        import maya.cmds as mc

        for grp in mc.ls(assemblies=True, long=True):
            if mc.ls(grp, dag=True, type="camera"):
                if grp in ['|top', '|front', '|side']:
                    continue

                instance = context.create_instance(
                    grp, family='ftrack.maya.camera'
                )

                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(FtrackPublishCollector)
pyblish.api.register_plugin(CollectCameras)

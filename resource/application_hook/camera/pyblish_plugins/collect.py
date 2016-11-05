# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api


class CollectCameras(pyblish.api.ContextPlugin):
    '''Collect cameras from Maya.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        import maya.cmds as mc

        for group in mc.ls(assemblies=True, long=True):
            if mc.ls(group, dag=True, type='camera'):
                if group in ['|top', '|front', '|side']:
                    continue

                instance = context.create_instance(
                    group, family='ftrack.maya.camera'
                )

                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(CollectCameras)

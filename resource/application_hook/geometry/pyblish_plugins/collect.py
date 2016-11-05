# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api


class CollectGeometries(pyblish.api.ContextPlugin):
    '''Collect maya geometry.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya mesh instances.'''
        import maya.cmds as mc

        for group in mc.ls(assemblies=True, long=True):
            if mc.ls(group, dag=True, type='mesh'):
                instance = context.create_instance(
                    group, family='ftrack.maya.geometry'
                )
                instance.data['publish'] = True
                instance.data['ftrack_components'] = []


pyblish.api.register_plugin(CollectGeometries)

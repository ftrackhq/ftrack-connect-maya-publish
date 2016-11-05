# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api


class CollectScene(pyblish.api.ContextPlugin):
    '''Collect maya scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add scene instances.'''
        instance = context.create_instance(
            'scene', family='ftrack.maya.scene'
        )
        instance.data['publish'] = True
        instance.data['ftrack_components'] = []

pyblish.api.register_plugin(CollectScene)

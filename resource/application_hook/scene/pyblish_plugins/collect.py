# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import logging

import pyblish.api


logger = logging.getLogger(__file__)


class CollectScene(pyblish.api.ContextPlugin):
    '''Collect maya scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add scene instances.'''
        logger.debug('Started collecting geometry from scene.')

        instance = context.create_instance(
            'scene', family='ftrack.maya.scene'
        )
        instance.data['publish'] = True
        instance.data['ftrack_components'] = []

        logger.debug('Collected scene instance {0!r}.'.format(instance))

pyblish.api.register_plugin(CollectScene)

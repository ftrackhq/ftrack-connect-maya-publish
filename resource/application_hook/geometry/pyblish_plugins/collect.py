# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import logging

import pyblish.api


logger = logging.getLogger(__file__)


class CollectGeometries(pyblish.api.ContextPlugin):
    '''Collect maya geometry.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya mesh instances.'''
        import maya.cmds as mc

        logger.debug('Started collecting geometry from scene.')

        for group in mc.ls(assemblies=True, long=True):
            if mc.ls(group, dag=True, type='mesh'):
                instance = context.create_instance(
                    group, family='ftrack.maya.geometry'
                )
                instance.data['publish'] = True
                instance.data['ftrack_components'] = []
                logger.debug(
                    'Collected geometry instance {0!r} {1!r}.'.format(
                        group, instance
                    )
                )


pyblish.api.register_plugin(CollectGeometries)

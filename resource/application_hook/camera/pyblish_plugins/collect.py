# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import logging

import pyblish.api


logger = logging.getLogger(__file__)


class CollectCameras(pyblish.api.ContextPlugin):
    '''Collect cameras from Maya.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        import maya.cmds as mc

        logger.debug('Started collecting camera from scene.')

        for group in mc.ls(assemblies=True, long=True):
            if mc.ls(group, dag=True, type='camera'):
                if group in ['|top', '|front', '|side']:
                    continue

                instance = context.create_instance(
                    group, family='ftrack.maya.camera'
                )

                instance.data['publish'] = True
                instance.data['ftrack_components'] = []

                logger.debug(
                    'Collected camera instance {0!r} {1!r}.'.format(
                        group, instance
                    )
                )


pyblish.api.register_plugin(CollectCameras)

# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api
from ftrack_connect_pipeline import constant


class CollectReviewableComponent(pyblish.api.ContextPlugin):
    '''Collect maya scene.'''

    order = pyblish.api.CollectorOrder

    def do_playblast(self):

        import maya.cmds as cmds
        import tempfile

        res_w = cmds.getAttr('defaultResolution.width')
        res_h = cmds.getAttr('defaultResolution.height')
        start_frame = cmds.playbackOptions(q=True, min=True)
        end_frame = cmds.playbackOptions(q=True, max=True)

        prev_selection = cmds.ls(sl=True)
        cmds.select(cl=True)

        filename = tempfile.NamedTemporaryFile(
            suffix='.mov', delete=False
        ).name

        cmds.playblast(
            format='qt',
            sequenceTime=0,
            clearCache=1,
            viewer=0,
            offScreen=True,
            showOrnaments=0,
            frame=range(int(start_frame), int(end_frame + 1)),
            rawFrameNumbers=True,
            filename=filename,
            fp=4,
            percent=100,
            compression="png",
            quality=70,
            w=res_w,
            h=res_h
        )

        if len(prev_selection):
            cmds.select(prev_selection)

        return start_frame

    def process(self, context):
        '''Process *context* and add scene instances.'''
        self.log.debug('Started collecting reviewable component.')

        instance = context.create_instance(
            'scene', families=['ftrack', 'scene']
        )
        instance.data['publish'] = True
        instance.data['ftrack_components'] = []
        instance.data['ftrack_reviewable_component'] = None

        make_reviewable = context.data['options'].get(
            constant.REVIEWABLE_COMPONENT_OPTION_NAME, 'False'
        )
        if make_reviewable:
            instance.data['ftrack_reviewable_component'] = self.do_playblast()
            self.log.debug(
                'Collected reviewable component from {0!r}.'.format(instance)

            )


pyblish.api.register_plugin(CollectReviewableComponent)

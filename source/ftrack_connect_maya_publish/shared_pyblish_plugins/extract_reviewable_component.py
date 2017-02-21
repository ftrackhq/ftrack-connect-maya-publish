# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import pyblish.api


class ExtractReviewableComponent(pyblish.api.InstancePlugin):
    '''Collect maya scene.'''

    order = pyblish.api.ExtractorOrder
    families = ['ftrack', 'reviewable']
    match = pyblish.api.Subset

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

        return filename

    def process(self, instance):
        '''Process *instance* and add scene instances.'''
        from ftrack_connect_pipeline import constant

        self.log.debug('Started collecting reviewable component.')
        make_reviewable = instance.context.data['options'].get(
            constant.REVIEWABLE_COMPONENT_OPTION_NAME, False
        )
        self.log.debug('is Make reviewable: %s' % make_reviewable)

        has_reviewable = instance.data.get('ftrack_reviewable_component')
        self.log.debug('Has reviewable: %s' % has_reviewable)

        if make_reviewable and not has_reviewable:
            self.log.warning('GENERATING PLAYBLAST')
            playblast_result = self.do_playblast()
            instance.data['ftrack_reviewable_component'] = playblast_result
            self.log.debug(
                'Collected reviewable component :{0:!r} from {1:!r}.'.format(
                    playblast_result, instance
                )

            )


pyblish.api.register_plugin(ExtractReviewableComponent)

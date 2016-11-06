# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import logging

import pyblish.api


logger = logging.getLogger(__file__)


class ExtractCameraMayaBinary(pyblish.api.InstancePlugin):
    '''Exctract camera as maya binary.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.maya.camera']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        import tempfile
        import maya.cmds as mc

        # Get the camera, either from the pre processor, if
        # bake or/and lock is selected, or the original one.
        baked_camera = instance.data.get('camera')
        camera = baked_camera or instance

        mc.select(str(camera), replace=True)

        context_options = instance.context.data['options'].get(
            'maya_binary', {}
        )
        logger.debug(
            'Started extracting camera {0!r} with options '
            '{1!r}.'.format(
                instance.name, context_options
            )
        )

        # Extract options and provide defaults.
        keep_reference = context_options.get('reference', False)
        keep_history = context_options.get('history', False)
        keep_channels = context_options.get('channels', False)
        keep_constraints = context_options.get('constraint', False)
        keep_expressions = context_options.get('expression', False)
        keep_shaders = context_options.get('shaders', True)
        export_selected = context_options.get('export_selected', True)

        # Generate temp file.
        temporary_path = tempfile.mkstemp(suffix='.mb')[-1]

        # Save maya file.
        mc.file(
            temporary_path,
            op='v=0',
            typ='mayaBinary',
            preserveReferences=keep_reference,
            constructionHistory=keep_history,
            channels=keep_channels,
            constraints=keep_constraints,
            expressions=keep_expressions,
            shader=keep_shaders,
            exportSelected=export_selected,
            exportAll=not export_selected,
            force=True
        )

        name = instance.name
        if name.startswith('|'):
            name = name[1:]

        new_component = {
            'name': '{0}.mayabinary'.format(name),
            'path': temporary_path,
        }

        instance.data['ftrack_components'].append(new_component)
        logger.debug(
            'Extracted {0!r} from {1!r}'.format(new_component, instance.name)
        )


pyblish.api.register_plugin(ExtractCameraMayaBinary)

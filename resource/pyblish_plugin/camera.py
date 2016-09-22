import pyblish.api


class CollectMayaCamera(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya scene.'''

        instance = context.create_instance(
            'maya.camera', family='ftrack.maya.camera'
        )

        instance.data['publish'] = True
        instance.data['options'] = {
            'start_frame': 0,
            'end_frame': 1,
            'include_mayabinary_camera': False,
            'bake_camera': False,
            'lock_camera': False,
            'history': False,
            'expression': False,
            'export_selected': False

        }
        instance.data['ftrack_components'] = []


class ExtractMayaCamera(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.camera']

    @classmethod
    def _ftrack_options(cls, instance):
        '''Return options.'''
        return [
            {
                'type': 'text',
                'label': 'Start Frame',
                'name': 'start_frame'
            },
            {
                'type': 'text',
                'label': 'End Frame',
                'name': 'end_frame'
            },
            {
                'type': 'boolean',
                'label': 'Include Maya Binary',
                'name': 'include_mayabinary_camera'
            },
            {
                'type': 'boolean',
                'label': 'Bake Camera',
                'name': 'bake_camera'
            },
            {
                'type': 'boolean',
                'label': 'Lock Camera',
                'name': 'lock_camera'
            },
            {
                'type': 'boolean',
                'label': 'History',
                'name': 'history'
            },
            {
                'type': 'boolean',
                'label': 'Expression',
                'name': 'expression'
            },
            {
                'type': 'boolean',
                'label': 'Export Selected',
                'name': 'export_selected'
            }
        ]

    def process(self, instance):
        import maya.cmds as mc
        import tempfile

        '''Process *instance* and extract media.'''
        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )

            # extract options
            keep_reference = instance.data['options']['reference']
            keep_history = instance.data['options']['history']
            keep_channels = instance.data['options']['channels']
            keep_constraints = instance.data['options']['constraint']
            keep_expressions = instance.data['options']['expression']
            keep_shaders = instance.data['options']['shaders']
            export_selected = instance.data['options']['export_selected']

            # generate temp file
            temporaryPath = tempfile.mkstemp(suffix='.mb')[-1]

            # create new maya file in temp
            mc.file(
                temporaryPath,
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
            new_component = {
                'name': instance.name,
                'path': temporaryPath,
            }

            instance.data['ftrack_components'].append(new_component)

import pyblish.api
import maya.cmds as mc
import tempfile


class CollecAlembic(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes fr`om scene.'''
    name = 'Publish write node content'
    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''

        instance = context.create_instance(
            'mayascene', family='ftrack.maya.alembic'
        )

        instance.data['publish'] = True

        instance.data['options'] = {
            'animation': False,
            'start_frame': 1,
            'end_frame': 1,
            'uv_write': True,
            'world_space': True,
            'write_visibility': True,
            'sampling': 1.00
        }
        instance.data['ftrack_components'] = []


class ExtractAlembicScene(pyblish.api.InstancePlugin):
    '''prepare component to be published'''

    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.alembic']

    @classmethod
    def _ftrack_options(cls, instance):
        '''Return options.'''
        return [
            {
                'type': 'boolean',
                'label': 'Include animation',
                'name': 'animation'
            },
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
                'label': 'UV Write',
                'name': 'uv_write'
            },
            {
                'type': 'boolean',
                'label': 'World Space',
                'name': 'world_space'
            },
            {
                'type': 'boolean',
                'label': 'Write Visibility',
                'name': 'write_visibility'
            },
            {
                'type': 'text',
                'label': 'Evaluate Every',
                'name': 'sampling'
            }
        ]

    def process(self, instance):
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
            keep_expressions = instance.data['options']['expressions']
            keep_shaders = instance.data['options']['shaders']
            attach_scene = instance.data['options']['attach_scene']

            temporaryPath = tempfile.NamedTemporaryFile(
                suffix='.mb', delete=False
            ).name

            # generate temp file
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
                # exportSelected=exportSelectedMode, # HOW DO I HAVE A SWITCH ?
                exportAll=attach_scene,
                force=True
            )

            instance.data['ftrack_components'].append(
                {
                    'name': instance.name,
                    'path': temporaryPath,
                }
            )


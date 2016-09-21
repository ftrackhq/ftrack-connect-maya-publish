import pyblish.api


class CollectMayaScene(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya scene.'''
        print 'COLLECTING MAYA SCENE'

        instance = context.create_instance(
            'maya.scene', family='ftrack.maya.scene'
        )

        instance.data['publish'] = True
        instance.data['options'] = {
            'reference': False,
            'history': False,
            'channels': False,
            'expression': False,
            'constraint': False,
            'shaders': True,
            'attach_scene': False,
            'export_selected': False
        }
        instance.data['ftrack_components'] = []


class ExtractMayaScene(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.scene']

    @classmethod
    def _ftrack_options(cls, instance):
        '''Return options.'''
        return [
            {
                'type': 'boolean',
                'label': 'Preserve reference',
                'name': 'reference'
            },
            {
                'type': 'boolean',
                'label': 'History',
                'name': 'history'
            },
            {
                'type': 'boolean',
                'label': 'Channels',
                'name': 'channels'
            },
            {
                'type': 'boolean',
                'label': 'Expressions',
                'name': 'expressions'
            },
            {
                'type': 'boolean',
                'label': 'Constraints',
                'name': 'constraint'
            },
            {
                'type': 'boolean',
                'label': 'Shaders',
                'name': 'shaders'
            },
            {
                'type': 'boolean',
                'label': 'Attach Scene',
                'name': 'attach_scene'
            },
            {
                'type': 'boolean',
                'label': 'Export Selected',
                'name': 'export_selected'
            }
        ]

    def process(self, instance):
        '''Process *instance* and extract media.'''
        print 'PROCESSING MAYA SCENE'

        import tempfile
        import maya.cmds as mc

        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )

            print 'INSIDE PROCESSING MAYA SCENE'

            print 1
            # extract options
            keep_reference = instance.data['options']['reference']
            keep_history = instance.data['options']['history']
            keep_channels = instance.data['options']['channels']
            keep_constraints = instance.data['options']['constraint']
            keep_expressions = instance.data['options']['expression']
            keep_shaders = instance.data['options']['shaders']
            attach_scene = instance.data['options']['attach_scene']
            export_selected = instance.data['options']['export_selected']

            print 2

            # generate temp file
            temporaryPath = tempfile.NamedTemporaryFile(
                suffix='.mb', delete=False
            ).name

            print 3

            # save maya file
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
                exportAll=attach_scene,
                force=True
            )
            print 4

            new_component = {
                'name': instance.name,
                'path': temporaryPath,
            }
            print 5

            print 'Adding new component: %s' % new_component
            instance.data['ftrack_components'].append(new_component)

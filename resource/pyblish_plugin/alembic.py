import pyblish.api


class CollectAlembic(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes fr`om scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        import maya.cmds as mc

        instance = context.create_instance(
            'maya.alembic', family='ftrack.maya.alembic'
        )

        instance.data['publish'] = True
        instance.data['options'] = {
            'animation': False,
            'uv_write': True,
            'world_space': True,
            'write_visibility': True,
            'sampling': 1.00,
            'start_frame': mc.playbackOptions(q=True, minTime=True),
            'end_frame': mc.playbackOptions(q=True, maxTime=True)
        }
        instance.data['ftrack_components'] = []


class ExtractAlembic(pyblish.api.InstancePlugin):
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
                'type': 'boolean',
                'label': 'UV Write',
                'name': 'uv_write'
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
            },
            {
                'type': 'boolean',
                'label': 'Export Selected',
                'name': 'export_selected'
            }
        ]

    def process(self, instance):
        '''Process *instance* and extract media.'''

        import maya.cmds as mc
        import tempfile

        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )

            # extract options
            animation = instance.data['options']['animation']
            uv_write = instance.data['options']['uv_write']
            start_frame = instance.data['options']['start_frame']
            end_frame = instance.data['options']['end_frame']
            world_space = instance.data['options']['world_space']
            write_visibility = instance.data['options']['write_visibility']
            sampling = instance.data['options']['sampling']
            export_selected = instance.data['options']['export_selected']

            # export alembic file
            temporaryPath = tempfile.mkstemp(suffix='.abc')[-1]

            if export_selected:
                nodes = mc.ls(sl=True, long=True)
                selectednodes = None
            else:
                selectednodes = mc.ls(sl=True, long=True)
                nodes = mc.ls(type='transform', long=True)

            objCommand = ''
            for n in nodes:
                objCommand = objCommand + '-root ' + n + ' '

            alembicJobArgs = ''

            if uv_write:
                alembicJobArgs += '-uvWrite '

            if world_space:
                alembicJobArgs += '-worldSpace '

            if write_visibility:
                alembicJobArgs += '-writeVisibility '

            if animation:
                alembicJobArgs += '-frameRange {0} {1} -step {2} '.format(
                    start_frame,
                    end_frame,
                    sampling
                )

            mc.loadPlugin('AbcExport.so', qt=1)

            alembicJobArgs += ' ' + objCommand + '-file ' + temporaryPath
            mc.AbcExport(j=alembicJobArgs)

            if selectednodes:
                mc.select(selectednodes)

            new_component = {
                'name': instance.name,
                'path': temporaryPath,
            }

            print 'Adding new component: %s' % new_component
            instance.data['ftrack_components'].append(new_component)

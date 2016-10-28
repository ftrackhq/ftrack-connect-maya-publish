import pyblish.api


class ExtractCameraAlembic(pyblish.api.InstancePlugin):
    '''Prepare component to be published.'''

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.maya.camera']

    def process(self, instance):
        '''Process *instance*.'''
        import maya.cmds as mc
        import tempfile
        mc.select(str(instance), replace=True)

        context_options = instance.context.data['options'].get(
            'alembic', {}
        )
        print (
            'Extracting Alembic using options:',
            context_options
        )

        currentStartFrame = mc.playbackOptions(min=True, q=True)
        currentEndFrame = mc.playbackOptions(max=True, q=True)

        # extract options
        animation = context_options.get('include_animation', False)
        uv_write = context_options.get('uv_write', True)
        start_frame = context_options.get('start_frame', currentStartFrame)
        end_frame = context_options.get('end_frame', currentEndFrame)
        world_space = context_options.get('world_space', True)
        write_visibility = context_options.get('write_visibility', True)
        sampling = context_options.get('sampling', 0.1)

        # export alembic file
        temporaryPath = tempfile.mkstemp(suffix='.abc')[-1]

        nodes = mc.ls(sl=True, long=True)

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

        name = instance.name
        if name.startswith('|'):
            name = name[1:]

        new_component = {
            'name': '%s.alembic' % name,
            'path': temporaryPath,
        }

        print 'Adding new component: %s' % new_component
        instance.data['ftrack_components'].append(new_component)


pyblish.api.register_plugin(ExtractCameraAlembic)

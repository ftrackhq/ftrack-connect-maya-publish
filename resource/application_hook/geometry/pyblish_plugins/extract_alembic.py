import pyblish.api


class ExtractAlembic(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.geometry']

    def process(self, instance):

        import maya.cmds as mc
        import tempfile

        mc.select(str(instance), replace=True)

        if instance.data.get('publish'):
            context_options = instance.context.data['options']
            print (
                'Extracting Alembic using options:',
                context_options
            )

            # extract options
            animation = context_options.get('animation', False)
            uv_write = context_options.get('uv_write', True)
            start_frame = context_options.get('start_frame', 0)
            end_frame = context_options.get('end_frame', 1)
            world_space = context_options.get('world_space', True)
            write_visibility = context_options.get('write_visibility', True)
            sampling = context_options.get('sampling', 0.1)
            export_selected = context_options.get('export_selected', True)

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
                'name': '%s.alembic' % instance.name,
                'path': temporaryPath,
            }

            print 'Adding new component: %s' % new_component
            instance.data['ftrack_components'].append(new_component)

pyblish.api.register_plugin(ExtractAlembic)

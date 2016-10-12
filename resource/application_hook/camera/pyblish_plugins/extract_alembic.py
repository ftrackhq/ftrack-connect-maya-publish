import pyblish.api


class ExtractAlembic(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.alembic.camera']

    def process(self, instance):

        import maya.cmds as mc
        import tempfile

        mc.select(str(instance), replace=True)

        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )

            # extract options
            animation = instance.data['options'].get('animation', False)
            uv_write = instance.data['options'].get('uv_write', True)
            start_frame = instance.data['options'].get('start_frame', 0)
            end_frame = instance.data['options'].get('end_frame', 1)
            world_space = instance.data['options'].get('world_space', True)
            write_visibility = instance.data['options'].get('write_visibility', True)
            sampling = instance.data['options'].get('sampling', 0.1)
            export_selected = instance.data['options'].get('export_selected', True)

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

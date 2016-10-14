import pyblish.api


class ExtractMayaBinary(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.camera']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        print 'PROCESSING MAYA BINARY', instance.data.get('publish')

        import tempfile
        import maya.cmds as mc

        # select the given geometries
        mc.select(str(instance), replace=True)

        context_options = instance.context.data['options'].get('maya_binary', {})
        print (
            'Extracting MayaBinary using options:',
            context_options
        )
        # extract options and provide defaults
        keep_reference = context_options.get('reference', False)
        keep_history = context_options.get('history', False)
        keep_channels = context_options.get('channels', False)
        keep_constraints = context_options.get('constraint', False)
        keep_expressions = context_options.get('expression', False)
        keep_shaders = context_options.get('shaders', True)
        export_selected = context_options.get('export_selected', True)

        # generate temp file
        temporaryPath = tempfile.mkstemp(suffix='.mb')[-1]

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
            exportAll=not export_selected,
            force=True
        )

        new_component = {
            'name': '%s.mayabinary' % instance.name,
            'path': temporaryPath,
        }

        print 'Adding new component: %s' % new_component
        instance.data['ftrack_components'].append(new_component)


pyblish.api.register_plugin(ExtractMayaBinary)

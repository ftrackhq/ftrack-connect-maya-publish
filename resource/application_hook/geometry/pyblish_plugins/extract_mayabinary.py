import pyblish.api


class ExtractMayaBinary(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.geometry']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        import tempfile
        import maya.cmds as mc

        # select the given geometries
        mc.select(str(instance), replace=True)

        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )

            # extract options and provide defaults
            keep_reference = instance.data['options'].get('reference', False)
            keep_history = instance.data['options'].get('history', False)
            keep_channels = instance.data['options'].get('channels', False)
            keep_constraints = instance.data['options'].get('constraint', False)
            keep_expressions = instance.data['options'].get('expression', False)
            keep_shaders = instance.data['options'].get('shaders', True)
            export_selected = instance.data['options'].get('export_selected', True)

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

            instance.data['ftrack_components'].append(new_component)


pyblish.api.register_plugin(ExtractMayaBinary)
import pyblish.api
import maya.cmds as cmds


class CollectGeometries(pyblish.api.ContextPlugin):

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        for grp in cmds.ls(assemblies=True, long=True):
            if cmds.ls(grp, dag=True, type="mesh"):
                instance = context.create_instance(
                    grp, family='ftrack.maya.geometry'
                )
                instance.data['ftrack_components'] = []


class ExtractGometries(pyblish.api.InstancePlugin):

    label = 'Maya binary'

    order = pyblish.api.ExtractorOrder

    families = ['ftrack.maya.geometry']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )
            instance.data['ftrack_components'].append(
                {
                    'name': instance.name,
                    'path': instance.data.get('options')['path'],
                }
            )

pyblish.api.register_plugin(CollectGeometries)
pyblish.api.register_plugin(ExtractGometries)

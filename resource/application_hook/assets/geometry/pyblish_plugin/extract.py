import pyblish.api
import nuke


class CollectWriteNode(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        for node in nuke.allNodes():
            if node.Class() == 'Write':
                instance = context.create_instance(node.name(), family='write')
                instance.data['publish'] = True
                instance.data['options'] = {
                    'path': node.knobs()['file'].value(),
                }
                instance.data['ftrack_components'] = []


class ExtractMedia(pyblish.api.InstancePlugin):
    '''Extract nuke media from scene.'''

    label = 'Maya binary'

    order = pyblish.api.ExtractorOrder

    families = ['write', 'read']

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

pyblish.api.register_plugin(CollectWriteNode)
pyblish.api.register_plugin(ExtractMedia)

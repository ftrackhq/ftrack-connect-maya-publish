import pyblish.api
import nuke


class CollectWriteNode(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes fr`om scene.'''
    name = 'Publish write node content'
    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''
        for node in nuke.allNodes():
            if node.Class() == 'Write':
                instance = context.create_instance(
                    node.name(), family='ftrack.write'
                )

                instance.data['publish'] = True
                instance.data['options'] = {
                    'path': node.knobs()['file'].value()
                }
                instance.data['ftrack_components'] = []


class ExtractMedia(pyblish.api.InstancePlugin):
    '''prepare component to be published'''

    order = pyblish.api.ExtractorOrder
    families = ['ftrack.write', 'ftrack.read']

    @classmethod
    def _ftrack_options(cls, instance):
        '''Return options.'''
        return [
            {
                'type': 'text',
                'label': 'Path',
                'name': 'path'
            }
        ]

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

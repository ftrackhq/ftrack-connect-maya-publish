import pyblish.api
import nuke


class CollectNukeScript(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes from scene.'''
    name = 'Publish current scene'
    order = pyblish.api.CollectorOrder

    def process(self, context):
        '''Process *context* and add maya camera instances.'''

        instance = context.create_instance(
            'mayascene', family='ftrack.mayascene'
        )

        instance.data['publish'] = True
        instance.data['options'] = {
            'script': nuke.root().knob('name').value()
        }
        instance.data['ftrack_components'] = []


class ExtractNukeScript(pyblish.api.InstancePlugin):
    '''prepare component to be published'''

    order = pyblish.api.ExtractorOrder
    families = ['ftrack.mayascene']

    @classmethod
    def _ftrack_options(cls, instance):
        '''Return options.'''
        return [
            {
                'type': 'text',
                'label': 'MayaScene',
                'name': 'script'
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
                    'path': instance.data.get('options')['script'],
                }
            )


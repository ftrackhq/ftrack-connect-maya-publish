# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import maya.cmds as cmds
import ftrack_connect_pipeline.asset


def filter_instances(pyblish_context):
    '''Return camera instances from *pyblish_context*.'''
    match = set(['light', 'ftrack'])
    return filter(
        lambda instance: match.issubset(instance.data['families']),
        pyblish_context
    )


class PublishLightRig(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya camera.'''

    def get_options(self):
        '''Return global options.'''
        options = [
            {
                'type': 'group',
                'label': 'Maya binary',
                'name': 'maya_binary',
                'options': [{
                    'name': 'reference',
                    'label': 'Reference',
                    'type': 'boolean',
                }, {
                    'name': 'history',
                    'label': 'History',
                    'type': 'boolean',
                }, {
                    'name': 'channels',
                    'label': 'Channels',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'expressions',
                    'label': 'Expressions',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'constraints',
                    'label': 'Constraints',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'shaders',
                    'label': 'Shaders',
                    'type': 'boolean',
                    'value': True

                }]
            }
        ]

        default_options = super(PublishLightRig, self).get_options()

        return default_options + options

    def get_publish_items(self):
        '''Return list of items that can be published.'''
        options = []
        for instance in filter_instances(self.pyblish_context):
            options.append(
                {
                    'label': instance.name,
                    'name': instance.id,
                    'value': instance.data.get('publish', False)
                }
            )

        return options

    def get_item_options(self, name):
        '''Return options for publishable item with *name*.'''
        options = []
        return options

    def get_scene_selection(self):
        '''Return a list of instance ids for scene selection.'''
        selection = cmds.ls(assemblies=True, long=True, sl=1)
        # Return list of instance ids for selected items in scene that match the
        # family.
        return [
            instance.id for instance in filter_instances(self.pyblish_context)
            if instance.name in selection
        ]

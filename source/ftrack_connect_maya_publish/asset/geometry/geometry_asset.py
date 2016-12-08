# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import ftrack_connect_pipeline.asset

import maya.cmds as cmds


class PublishGeometry(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya geometry.'''

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
            },
            {
                'type': 'group',
                'label': 'Alembic',
                'name': 'alembic',
                'options': [{
                    'name': 'include_animation',
                    'label': 'Include animation',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'uv_write',
                    'label': 'UV write',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'world_space',
                    'label': 'World space',
                    'type': 'boolean',
                    'value': True
                }, {
                    'name': 'write_visibility',
                    'label': 'Write visibility',
                    'type': 'boolean',
                    'value': True
                }]
            }
        ]

        default_options = super(PublishGeometry, self).get_options()

        return default_options + options

    def get_publish_items(self):
        '''Return list of items that can be published.'''
        match = set(['geometry', 'ftrack'])

        options = []
        for instance in self.pyblish_context:
            if match.issubset(instance.data['families']):
                options.append(
                    {
                        'label': instance.name,
                        'name': instance.name,
                        'value': instance.data.get('publish', False)
                    }
                )

        return options

    def get_item_options(self, name):
        '''Return options for publishable item with *name*.'''
        return []

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        return cmds.ls(assemblies=True, long=True, sl=1)

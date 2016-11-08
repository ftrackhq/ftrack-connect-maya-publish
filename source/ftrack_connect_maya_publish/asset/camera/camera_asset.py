# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import maya.cmds as cmds
import ftrack_connect_pipeline.asset


class PublishCamera(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya camera.'''

    def get_options(self, publish_data):
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
            },
            {
                'type': 'group',
                'label': 'Camera options',
                'name': 'camera_options',
                'options': [{
                    'name': 'lock',
                    'label': 'Lock',
                    'type': 'boolean'
                }, {
                    'name': 'bake',
                    'label': 'Bake',
                    'type': 'boolean'
                }]
            }
        ]

        default_options = super(
            PublishCamera, self
        ).get_options(publish_data)

        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.maya.camera',):
                options.append(
                    {
                        'label': instance.name,
                        'name': instance.name,
                        'value': True
                    }
                )

        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''
        options = []
        return options

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        return cmds.ls(assemblies=True, long=True, sl=1)

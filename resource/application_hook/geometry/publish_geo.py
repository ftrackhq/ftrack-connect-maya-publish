import ftrack_api

import ftrack_connect_pipeline.asset
IDENTIFIER = 'geometry'

import maya.cmds as cmds


class PublishGeometry(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya image.'''

    def get_options(self, publish_data):
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
                }, {
                    'name': 'expressions',
                    'label': 'Expressions',
                    'type': 'boolean',
                }, {
                    'name': 'constraints',
                    'label': 'Constraints',
                    'type': 'boolean',
                }, {
                    'name': 'shaders',
                    'label': 'Shaders',
                    'type': 'boolean',
                }, {
                    'name': 'export_selected',
                    'label': 'Export selected',
                    'type': 'boolean',
                }]
            },
            {
                'type': 'group',
                'label': 'Alembic',
                'name': 'alembic',
                'options': [{
                    'name': 'include_animation',
                    'label': 'Include animation',
                    'type': 'boolean'
                }, {
                    'name': 'uv_write',
                    'label': 'UV write',
                    'type': 'boolean'
                }, {
                    'name': 'world_space',
                    'label': 'World space',
                    'type': 'boolean'
                }, {
                    'name': 'write_visibility',
                    'label': 'Write visibility',
                    'type': 'boolean'
                }]
            }
        ]

        default_options = super(
            PublishGeometry, self
        ).get_options(publish_data)

        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''

        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.maya.geometry',):
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
        # print 'get_item_options', publish_data

        return []

    def get_scene_selection(self):
        '''Return a list of names for scene selection.'''
        return cmds.ls(assemblies=True, long=True, sl=1)


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishGeometry(
            label='Geometry',
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9cz/EzE/9czEzE8yi.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)

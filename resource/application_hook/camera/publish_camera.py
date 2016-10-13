import ftrack_api

import ftrack_connect_pipeline.asset
IDENTIFIER = 'camera'


class PublishCamera(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya image.'''

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
                    'label': 'include_animation',
                    'type': 'boolean'
                }, {
                    'name': 'uv_write',
                    'label': 'uv_write',
                    'type': 'boolean'
                }, {
                    'name': 'world_space',
                    'label': 'world_space',
                    'type': 'boolean'
                }, {
                    'name': 'write_visibility',
                    'label': 'write_visibility',
                    'type': 'boolean'
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
                    'name': 'Bake',
                    'label': 'bake',
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
                        'name': instance.id,
                        'value': True
                    }
                )

        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''
        options = []
        return options


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishCamera(
            label='Camera',
            description='publish camera to ftrack.',
            icon='http://www.clipartbest.com/cliparts/LiK/dLB/LiKdLB6zT.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)

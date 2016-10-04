import ftrack_api

import ftrack_connect_pipeline.asset

IDENTIFIER = 'geometry'


class PublishGeometry(ftrack_connect_pipeline.asset.PublishAsset):
    '''Handle publish of maya geometry.'''

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = [
            {
                'type': 'boolean',
                'label': 'Publish Maya Binary',
                'name': 'maya.binary'
            },
            {
                'type': 'boolean',
                'label': 'Publish Alembic',
                'name': 'maya.alembic'
            }
        ]
        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''

        options = {
            'maya.binary': [
                {
                    'type': 'boolean',
                    'label': 'Preserve reference',
                    'name': 'reference'
                },
                {
                    'type': 'boolean',
                    'label': 'History',
                    'name': 'history'
                },
                {
                    'type': 'boolean',
                    'label': 'Channels',
                    'name': 'channels'
                },
                {
                    'type': 'boolean',
                    'label': 'Expressions',
                    'name': 'expressions'
                },
                {
                    'type': 'boolean',
                    'label': 'Constraints',
                    'name': 'constraint'
                },
                {
                    'type': 'boolean',
                    'label': 'Shaders',
                    'name': 'shaders'
                },
                {
                    'type': 'boolean',
                    'label': 'Export Selected',
                    'name': 'export_selected'
                }
            ],
            'maya.alembic': [
                {
                    'type': 'boolean',
                    'label': 'Include animation',
                    'name': 'animation'
                },
                {
                    'type': 'boolean',
                    'label': 'UV Write',
                    'name': 'uv_write'
                },
                {
                    'type': 'text',
                    'label': 'Start Frame',
                    'name': 'start_frame'
                },
                {
                    'type': 'text',
                    'label': 'End Frame',
                    'name': 'end_frame'
                },
                {
                    'type': 'boolean',
                    'label': 'World Space',
                    'name': 'world_space'
                },
                {
                    'type': 'boolean',
                    'label': 'Write Visibility',
                    'name': 'write_visibility'
                },
                {
                    'type': 'text',
                    'label': 'Evaluate Every',
                    'name': 'sampling'
                },
                {
                    'type': 'boolean',
                    'label': 'Export Selected',
                    'name': 'export_selected'
                }
            ]
        }

        return options.get(name, [])


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishGeometry(
            label=IDENTIFIER,
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)

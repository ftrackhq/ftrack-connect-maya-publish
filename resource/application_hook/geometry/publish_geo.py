import ftrack_api

import ftrack_connect_pipeline.asset

IDENTIFIER = 'geometry'


class PublishGeometry(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya image.'''

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.maya.geometry', ):
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
        for instance in publish_data:
            if instance.id == name:
                return [
                    {
                        'type': 'boolean',
                        'label': 'Preserve reference',
                        'name': 'reference',
                        'value': False
                    },
                    {
                        'type': 'boolean',
                        'label': 'History',
                        'name': 'history',
                        'value': False
                    },
                    {
                        'type': 'boolean',
                        'label': 'Channels',
                        'name': 'channels',
                        'value': False
                    },
                    {
                        'type': 'boolean',
                        'label': 'Expressions',
                        'name': 'expressions',
                        'value': False
                    },
                    {
                        'type': 'boolean',
                        'label': 'Constraints',
                        'name': 'constraint',
                        'value': False
                    },
                    {
                        'type': 'boolean',
                        'label': 'Shaders',
                        'name': 'shaders',
                        'value': True
                    },
                    {
                        'type': 'boolean',
                        'label': 'Export Selected',
                        'name': 'export_selected',
                        'value': False
                    }
                ]

        return []


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishGeometry(
            label='Geometry',
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)

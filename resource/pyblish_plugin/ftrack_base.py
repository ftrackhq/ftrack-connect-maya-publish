import os

import pyblish.api
import ftrack_api


class FtrackPublishCollector(pyblish.api.ContextPlugin):
    '''Prepare ftrack publish.'''

    order = pyblish.api.CollectorOrder

    def process(self, context):
        print 'COLLECT CONTEXT'

        '''Process *context* and add ftrack entity.'''
        session = ftrack_api.Session()
        ftrack_entity = session.get(
            'Context', os.environ['FTRACK_CONTEXT_ID']
        )
        context.data['ftrack_entity'] = ftrack_entity


class IntegratorCreateAsset(pyblish.api.ContextPlugin):
    '''Create asset and prepare publish.'''

    order = pyblish.api.IntegratorOrder
    families = ['ftrack.maya.*']

    @classmethod
    def _ftrack_options(cls, context):
        '''Return options.'''
        from ftrack_connect_pipeline.ui.widget import asset_selector
        asset_selector = asset_selector.AssetSelector(
            context.data['ftrack_entity']
        )

        def handle_change(value):
            context.data['options'] = {}
            context.data['options']['asset_name'] = value['asset_name']
            context.data['options']['asset_type'] = value['asset_type']

        asset_selector.asset_changed.connect(handle_change)

        return asset_selector

    def process(self, context):
        print 'CREATEA ASSET'

        '''Process *context* create asset.'''
        ftrack_entity = context.data['ftrack_entity']
        session = ftrack_entity.session

        asset_type_id = context.data['options']['asset_type']
        asset_name = context.data['options']['asset_name']
        context_id = ftrack_entity['id']

        asset = session.query(
            'Asset where context_id is "{0}" and name is "{1}" and '
            'type_id is "{2}"'.format(
                context_id, asset_name, asset_type_id
            )
        ).first()

        if asset is None:
            asset = session.create(
                'Asset',
                {
                    'context_id': context_id,
                    'type_id': asset_type_id,
                    'name': asset_name
                }
            )

        # Create an asset version in a pre-published state.
        asset_version = session.create(
            'AssetVersion',
            {
                'asset': asset,
                'is_published': False
            }
        )

        session.commit()

        context.data['asset_version'] = asset_version

        print (
            'Integrating with options',
            asset_version,
            context.data.get('options', {}),
            context.data.get('ftrack_entity'),
            list(context)
        )


class IntegratorCreateComponents(pyblish.api.InstancePlugin):
    '''Extract maya cameras from scene.'''

    order = pyblish.api.IntegratorOrder + 0.1

    # THESE ARE NOT WORKING BUT THEY SHOULD FILTER !
    # families = ['ftrack.maya.*']
    # families = ['ftrack.*']

    families = ['*']

    def process(self, instance):
        '''Process *instance* and create components.'''
        print 'CREATE COMPONENT'

        context = instance.context
        asset_version = context.data['asset_version']
        session = asset_version.session
        location = session.pick_location()
        for component_item in instance.data.get('ftrack_components', []):
            session.create_component(
                component_item['path'],
                {
                    'version_id': asset_version['id'],
                    'name': component_item['name']
                },
                location=location
            )

        session.commit()


class IntegratorPublishVersion(pyblish.api.ContextPlugin):
    '''Mark asset version as published.'''

    order = pyblish.api.IntegratorOrder + 0.2

    def process(self, context):
        print 'PUBLISHING VERSION'

        '''Process *context*.'''
        asset_version = context.data['asset_version']
        session = asset_version.session

        asset_version['is_published'] = True
        session.commit()

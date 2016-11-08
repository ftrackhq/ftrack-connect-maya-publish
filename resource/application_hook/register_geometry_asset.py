# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_maya_publish.asset.geometry import geometry_asset


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    geometry = ftrack_connect_pipeline.asset.Asset(
        identifier='geometry',
        publish_asset=geometry_asset.PublishGeometry(
            label='Geometry',
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9cz/EzE/9czEzE8yi.png'
        )
    )
    geometry.register(session)


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.register-assets',
        functools.partial(register_asset_plugin, session)
    )

# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_maya_publish.asset.camera import camera_asset


def create_asset_publish():
    '''Return asset publisher.'''
    return camera_asset.PublishCamera(
        description='publish camera to ftrack.',
    )


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    camera = ftrack_connect_pipeline.asset.Asset(
        identifier='camera',
        label='Camera',
        icon='http://www.clipartbest.com/cliparts/LiK/dLB/LiKdLB6zT.png',
        create_asset_publish=create_asset_publish
    )
    camera.register(session)


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.register-assets',
        functools.partial(register_asset_plugin, session)
    )

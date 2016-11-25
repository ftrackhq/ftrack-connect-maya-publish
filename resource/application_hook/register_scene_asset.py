# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_maya_publish.asset.scene import scene_asset


def create_asset_publish():
    '''Return asset publisher.'''
    return scene_asset.PublishScene(
        description='publish maya scene to ftrack.',
        enable_scene_as_reference=False
    )


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    scene = ftrack_connect_pipeline.asset.Asset(
        identifier='scene',
        label='Scene',
        icon='http://www.clipartbest.com/cliparts/ace/Brb/aceBrbBc4.png',
        create_asset_publish=create_asset_publish
    )
    scene.register(session)


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.register-assets',
        functools.partial(register_asset_plugin, session)
    )

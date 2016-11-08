# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_maya_publish.asset.scene import scene_asset


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    scene = ftrack_connect_pipeline.asset.Asset(
        identifier='scene',
        publish_asset=scene_asset.PublishScene(
            label='Scene',
            description='publish maya scene to ftrack.',
            icon='http://www.clipartbest.com/cliparts/ace/Brb/aceBrbBc4.png'
        )
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

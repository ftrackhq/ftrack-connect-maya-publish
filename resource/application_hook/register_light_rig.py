# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import functools

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_maya_publish.asset.light_rig import light_rig_asset


FTRACK_ASSET_TYPE = 'lgt'


def create_asset_publish():
    '''Return asset publisher.'''
    return light_rig_asset.PublishLightRig(
        description='publish light rig to ftrack.',
        asset_type_short=FTRACK_ASSET_TYPE

    )


def register_asset_plugin(session, event):
    '''Register asset plugin.'''
    camera = ftrack_connect_pipeline.asset.Asset(
        identifier=FTRACK_ASSET_TYPE,
        label='LightRig',
        icon='http://www.clipartbest.com/cliparts/9c4/6ep/9c46ep5di.jpg',
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

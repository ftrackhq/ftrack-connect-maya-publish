# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_maya_publish.asset import scene_asset


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    scene = ftrack_connect_pipeline.asset.Asset(
        identifier='scene',
        publish_asset=scene_asset.PublishScene(
            label='Scene',
            description='publish maya scene to ftrack.',
            icon='http://www.clipartbest.com/cliparts/ace/Brb/aceBrbBc4.png'
        )
    )
    scene.register(session)

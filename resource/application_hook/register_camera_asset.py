# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import ftrack_api
import ftrack_connect_pipeline.asset

from ftrack_connect_maya_publish.asset import camera_asset


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    camera = ftrack_connect_pipeline.asset.Asset(
        identifier='camera',
        publish_asset=camera_asset.PublishCamera(
            label='Camera',
            description='publish camera to ftrack.',
            icon='http://www.clipartbest.com/cliparts/LiK/dLB/LiKdLB6zT.png'
        )
    )
    camera.register(session)

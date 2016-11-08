
import ftrack_api
import ftrack_connect_pipeline.asset
import ftrack_connect_maya_publish.asset.camera_asset


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier='camera',
        publish_asset=ftrack_connect_maya_publish.asset.camera.camera_asset.PublishCamera(
            label='Camera',
            description='publish camera to ftrack.',
            icon='http://www.clipartbest.com/cliparts/LiK/dLB/LiKdLB6zT.png'
        )
    )
    image_asset.register(session)

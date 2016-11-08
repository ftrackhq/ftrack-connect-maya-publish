import ftrack_api
import ftrack_connect_pipeline.asset
import ftrack_connect_maya_publish.asset.scene_asset


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    geometry_asset = ftrack_connect_pipeline.asset.Asset(
        identifier='scene',
        publish_asset=ftrack_connect_maya_publish.asset.scene.scene_asset.PublishScene(
            label='Scene',
            description='publish maya scene to ftrack.',
            icon='http://www.clipartbest.com/cliparts/ace/Brb/aceBrbBc4.png'
        )
    )
    geometry_asset.register(session)

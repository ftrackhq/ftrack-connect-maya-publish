import ftrack_api
import ftrack_connect_pipeline.asset
import ftrack_connect_maya_publish.asset.geometry_asset


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    geometry_asset = ftrack_connect_pipeline.asset.Asset(
        identifier='geometry',
        publish_asset=ftrack_connect_maya_publish.asset.geometry.geometry_asset.PublishGeometry(
            label='Geometry',
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9cz/EzE/9czEzE8yi.png'
        )
    )
    geometry_asset.register(session)

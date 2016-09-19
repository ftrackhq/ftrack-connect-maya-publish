import ftrack_api

import ftrack_connect_pipeline.ui.publish_dialog
import ftrack_connect_pipeline.util
import ftrack_connect_pipeline.ui.widget


identifier = 'ftrack-publish-publish-media-action'


def open_dialog():
    '''Open dialog.'''
    dialog = ftrack_connect_pipeline.ui.publish_dialog.PublishDialog(
        label='Media',
        description=(
            'from here you can select and publish any media from nuke to '
            'ftrack.'
        ),
        instance_filter=(
            lambda instance: True
        )
    )
    dialog.exec_()


def discover(event):
    '''Return action based on *event*.'''
    item = {
        'items': [{
            'label': 'Media',
            'icon': 'http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png',
            'actionIdentifier': identifier
        }]
    }

    return item


def launch(event):
    '''Callback method for publish action.'''
    ftrack_connect_pipeline.util.invoke_in_main_thread(open_dialog)

    return {
        'success': True,
        'message': 'Custom publish action started successfully!'
    }


def register(session, **kw):
    '''Register action.'''
    if not isinstance(session, ftrack_api.Session):
        return

    session.event_hub.subscribe(
        'topic=ftrack.action.discover',
        discover
    )

    session.event_hub.subscribe(
        'topic=ftrack.action.launch and data.actionIdentifier={0}'.format(
            identifier
        ),
        launch
    )

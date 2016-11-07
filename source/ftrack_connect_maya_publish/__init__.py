# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import functools

import pyblish.plugin
import ftrack_api.event.base

from ._version import __version__

from ftrack_connect_maya_publish.asset.camera import camera_asset
from ftrack_connect_maya_publish.asset.geometry import geometry_asset
from ftrack_connect_maya_publish.asset.scene import scene_asset


def register_callback(session, event):
    '''Handle register event.'''
    print 'Callback on', session
    camera_asset.register(session)
    geometry_asset.register(session)
    scene_asset.register(session)

    path = os.path.normpath(
        os.path.join(
            os.path.abspath(
                os.path.dirname(
                    __file__
                )
            ),
            'common_pyblish_plugins'
        )
    )

    print 'Register plugin path', path
    pyblish.plugin.register_plugin_path(path)


def register_assets(session):
    '''Register by emitting event on *session*.'''
    print 'Register listener on session', session

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.register-assets',
        functools.partial(register_callback, session)
    )

    session.event_hub.publish(
        ftrack_api.event.base.Event(
            topic='ftrack.pipeline.register-assets',
            data=dict()
        ),
        synchronous=True
    )

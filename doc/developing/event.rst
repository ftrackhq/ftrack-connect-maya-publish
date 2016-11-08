..
    :copyright: Copyright (c) 2016 ftrack

.. _developing/event:

***********
Events list
***********

The following are standard ftrack events published by the framework.

.. _developing/event/ftrack.pipeline.register-assets:

ftrack.pipeline.register-assets
===============================

Emitted by the framework when it requires the assets to register to the given
session. The event is emitted synchronous::

    Event(
        topic='ftrack.pipeline.register-assets',
        data=dict()
    )

A common use is to register using the `ftrack_connect_pipeline.asset.Asset`::

    geometry = ftrack_connect_pipeline.asset.Asset(
        identifier='geometry',
        publish_asset=geometry_asset.PublishGeometry(
            label='Geometry',
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9cz/EzE/9czEzE8yi.png'
        )
    )
    geometry.register(session)

Where geometry.register will attach relevant event / action listeners.

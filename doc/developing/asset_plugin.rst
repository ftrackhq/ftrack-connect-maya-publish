..
    :copyright: Copyright (c) 2016 ftrack

.. _developing/asset_plugin:

************
Asset plugin
************

The publishing and later importing and switching of an asset version is governed
by the definition of an asset plugin. The idea is to allow 3rd party integrators
to write custom asset plugins or extend existing ones.

Bundled assets plugins are based on class definitions in
`source/ftrack_connect_maya_publish/asset` of the `ftrack-connect-maya-publish`
repository. However, they will register from event plugins in the `resource`
directory when the application ftrack-python-api session emits the
:ref:`developing/event/ftrack.pipeline.register-assets` event.

An asset plugin will contain the following functionality:

*   Publish asset version (Available now)
*   Import asset version (Available later)
*   Switch asset version (Available later)

Pipeline repository
===================

The new repository, https://bitbucket.org/ftrack/ftrack-connect-pipeline,
contains widgets, asset base classes and other utils that will be reused in
ftrack pipeline tools and integrations.

Notable classes are those defined in `source/ftrack_connect_pipeline/asset/`


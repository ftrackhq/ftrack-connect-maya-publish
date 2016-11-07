..
    :copyright: Copyright (c) 2016 ftrack

***********
Development
***********

This is a WIP article to give some background on how the new publish tools
works internally. At the moment it is mostly focused on the :term:`pyblish` way
of publishing data using the :term:`publish dialog`, even though :term:`pyblish`
is not a requirement when developing your own `Publish action`.

After reading this article you should have a basic understanding of how it works
and how to extend it.

A Connect plugin
================

The publish tool is built as a plugin to :term:`ftrack connect`. As such it can
be checked out and run from source. See :ref:`installation` for more details.

Hooking into maya launch
========================

The `hook/listen_to_maya_launch.py` will hook into the
`ftrack.connect.application.launch` and modify environment variables to load
the plugin and dependencies.

Concept of an asset
===================

The publishing and later loading and switching of an asset is governed by the
definition of an asset. The idea is to allow 3rd party integrators to write 
custom assets or extend existing ones.

Bundled assets are placed in `resource/application_hook/` of the
`ftrack-connect-maya-publish` repository. The :env:`FTRACK_EVENT_PLUGIN_PATH`
is pointed to this directory and the assets themselves are implemented as
event plugins.

As an example we will look at the geometry asset which uses :term:`pyblish` for
publishing. This is the structure of the asset plugin::

    resource/application_hook/geometry/
        pyblish_plugins/
            collect.py
            extract_alembic.py
            extract_mayabinary.py
        geometry_asset.py

In the `pyblish_plugins` directory there are a number of pyblish plugins
defined, more on this later.

In the `geometry_asset.py` we define the asset, how it is published, imported
and how to switch it to a different version if already imported. The asset
does not necessarily have to be published using :term:`pyblish` but in this
article we assume that :term:`pyblish` is used.

Let us look more at geometry_asset.py source:

.. literalinclude:: /resource/geometry_asset_example.py
    :language: python

At the bottom we find registration of the asset:

.. literalinclude:: /resource/geometry_asset_example.py
    :lines: 110-

The asset will have a unique identifier, in this case `geometry` and a
publish_asset argument. The `PublishGeometry` instance will handle publishing
of the asset. In future versions there will be a import_asset and a
switch_asset argument.

Let us look at a definition of the PublishGeometry class:

.. literalinclude:: /resource/geometry_asset_example.py
    :lines: 10-13

Here we see that it inherits `ftrack_connect_pipeline.asset.PyblishAsset` and
will, as the name suggests be using :term:`pyblish` for the publishing process.

While publishing the :term:`pyblish` plugins will be accessing options from the
interface. These options are defined in the methods on the `PublishGeometry`
class and and are following the syntax described in
:ref:`Developing actions user interface <developing/actions/user-interface>`.

Notable methods that are implemented on the `PublishGeometry` class:

:get_publish_items:
    Return a list of items that can be published from the scene. In a pyblish
    based publish workflow this is ususally done by filtering on the pyblish
    instance family/families.

    The method takes a `publish_data` argument which in this case is a
    :term:`pyblish` context.
:get_options:
    Return a list of options that are general options for the publish.

    The method takes a `publish_data` argument which in this case is a
    :term:`pyblish` context.
:get_item_options:
    Return a list of options that are valid for the given item name.

    The method takes a `publish_data` argument which in this case is a
    :term:`pyblish` context.

Publishing with pyblish
-----------------------

In the `pyblish_plugins` directory we have the plugins that will collect the
geometries from the scene and extract them as a maya binary and/or alembic.

Common :term:`pyblish` plugins are defined in
`repository-root/application_hook/pyblish_plugins` and will be used for common
collect and integration plugins.

Pipeline repository
===================

The new repository, https://bitbucket.org/ftrack/ftrack-connect-pipeline,
contains widgets, asset base classes and other utils that will be reused in
ftrack pipeline tools and integrations.

Notable classes are those defined in `source/ftrack_connect_pipeline/asset/`

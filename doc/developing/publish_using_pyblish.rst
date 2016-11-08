..
    :copyright: Copyright (c) 2016 ftrack

.. _developing/publish_using_pyblish:

************************
Publishing using pyblish
************************

As an example we will look at the geometry asset which uses :term:`pyblish` for
publishing. This is the structure of the asset plugin::

    ftrack_connect_maya_publish/asset/geometry/
        pyblish_plugins/
            collect.py
            extract_alembic.py
            extract_mayabinary.py
        geometry_asset.py

In the `pyblish_plugins` directory there are a number of pyblish plugins
defined, more on this later.

In the `geometry_asset.py` we define the asset plugin, how it is published,
imported and how to switch it to a different version if already imported. The
asset plugin does not necessarily have to be published using :term:`pyblish` but
in this article we assume that :term:`pyblish` is used.

Let us look more at geometry_asset.py source:

.. literalinclude:: /resource/geometry_asset_example.py
    :language: python

At the bottom we find the registration of the asset plugin:

.. literalinclude:: /resource/geometry_asset_example.py
    :lines: 110-

The asset plugin will have a unique identifier, in this case `geometry` and a
publish_asset argument. The `PublishGeometry` instance will handle publishing.

.. note::

    In future versions there will be a import_asset and a switch_asset argument.

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

Pyblish plugins
---------------

In the `pyblish_plugins` directory we have the plugins that will collect the
geometries from the scene and extract them as a maya binary and/or alembic.

Common :term:`pyblish` plugins are defined in
`ftrack_connect_maya_publish/common_pyblish_plugins` and will be used for
collection and integration plugins that are shared between asset plugins.

..
    :copyright: Copyright (c) 2016 ftrack

***********
Development
***********

This is a WIP article to give some background on how the new publish tools
works internally. 

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
custom assets or extend existing ones. A

Bundled assets are placed in `resource/application_hook/` of the
`ftrack-connect-maya-publish` repository.

E.g. the Geometry asset that uses :term:`pyblish` for publishing has this
structure::

    resource/application_hook/geometry/
        pyblish_plugins/
            collect.py
            extract_alembic.py
            extract_mayabinary.py
        publish_geo.py



Pyblish
-------

Pipeline repository

Event hooks

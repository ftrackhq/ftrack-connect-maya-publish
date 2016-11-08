..
    :copyright: Copyright (c) 2016 ftrack

.. _developing/overview:

********
Overview
********

A Connect plugin
================

The new publish tools are built as a plugin to :term:`ftrack connect`. As
such they can be checked out and run from source. See :ref:`installation` for
more details.

Hooking into maya launch
========================

The `hook/listen_to_maya_launch.py` in the repository root will hook into the
`ftrack.connect.application.launch` and modify environment variables to load
the plugin and dependencies.

..
    :copyright: Copyright (c) 2016 ftrack

***************************
Overview and preview notice
***************************

The current iteration of the ftrack Connect integrations has been with us for
a few years and now is the time to make a bigger overhaul of the tools.

Our goal is to refresh the integrations overall, starting with the publishing
dialog. Future iterations will provide better Import and Asset switching, but
also new features like switching between tasks without closing and reopening the
application.

Note that the state of this tool is currently a development preview and should
*not* be used in production.

What is this?
=============

In the first iteration we are focusing on the publish dialog. In Maya you will
find a new dropdown menu next to ftrack called `ftrack new`. From here you can
launch different `publish actions`.

At the moment there are a limited set of different actions to pick from. Please
see :ref:`usage` for a complete list.

The publish process is built on top of :term:`pyblish` but is not immediately
obvious to the end-user. The :term:`publish dialog` is developed separately by
ftrack an can be used together with or without :term:`pyblish`.

.. seealso:

    To learn more about  :term:`pyblish`, how publishing works under the hood
    and how to extend it. Please refer to the :ref:`development` article.

Limitations and the bright future
=================================

At the moment there are several limitations of the :term:`publish dialog` and
it should be seen as a preview of what is coming. Neither design, nor features
are a representation of what will be in the final version.

This is a list of notes and limitations for the current iteration of the tools:

*   Maya can only publish Camera, Geometry and Scene.
*   The formatts, alembic and maya binary cannot be disabled and both are always
    published.
*   Not possible to set the thumbnail on the publish.
*   Not possible to see or switch context of the publish.
*   No feedback if asset is not selected when publishing. At the moment this
    will result in a failed publish.
*   Not possible to go back and change settings if publish fails.
*   The :term:`asset type` will be selected based on what you want to publish,
    but you are not restricted to this type. It does however affect the ability
    to import using the current version of the importer. To publish a `Camera`
    and allow import choose `Camera` asset type when publsihing, for `Geometry`
    choose `Geometry` and so on.

Below is a list of limitations in regards to the Developer / TD aspect of the
tool:

*   At the moment there are not good :term:`event hooks` to use. Examples that
    we may support.
*   Validation :term:`pyblish plugin` are not yet supported.
*   The shipped :term:`pyblish plugin` are sourced by the
    :term:`ftrack-python-api` rather than when calling
    `pyblish.plugin.register_plugin_path`.
*   Current iterations of the :term:`Import dialog` cannot imported published
    alembics.

Feedback
========

Please add relevant feedback to the `beta forum <http://forum.ftrack.com/>` or
contact support@ftrack.com.

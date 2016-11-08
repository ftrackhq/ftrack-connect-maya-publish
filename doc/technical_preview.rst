..
    :copyright: Copyright (c) 2016 ftrack

.. _technical_preview:

************************
Technical preview notice
************************

In the first iteration we are focusing on the publish dialog. In Maya you will
find a new dropdown menu next to ftrack called :guilabel:`ftrack new`. From here
you can launch :term:`publish actions <publish action>` registered by
:term:`asset plugins <asset plugin>`.

In the first version there is a limited set of actions to pick from. Please see
:ref:`usage` for a complete list of :term:`asset plugins <asset plugin>`.

The publish process can be built on top of :term:`pyblish`, but this is not
immediately obvious to the end-user since the :term:`pyblish` user interface
is not used. Instead a :term:`publish dialog` is developed separately by
ftrack an can be used together with :term:`pyblish`, or standalone. All
:term:`publish actions <publish action>` that are bundled with Maya are however
based on :term:`pyblish`.

.. seealso::

    To learn more about :term:`pyblish`, how publishing works under the hood
    and how to extend it. Please refer to the :ref:`developing` article.

.. _technical_preview/limitations:

Limitations and the bright future
---------------------------------

At the moment there are several limitations of the :term:`publish dialog` and
it should be seen as a preview of what is coming. Neither design, nor features
represents what will be in the final version.

This is a list of notes and limitations for the current iteration of the tools
that is likely to be solved before the final release:

*   Maya can only publish a limited set of assets, see :ref:`usage`.
*   The alembic and maya binary format cannot be disabled and both are always
    published.
*   It is not possible to set the thumbnail when publishing.
*   It is not possible to see or switch context of the publish.
*   No feedback is given if an ftrack asset is not selected when publishing. At
    the moment this will result in a failed publish.
*   It is not possible to go back and change settings if a publish fails.
*   The :term:`asset type` will be selected based on what you want to publish,
    but you are not restricted to this type. It does however affect the ability
    to import using the current version of the :term:`import dialog`. To publish
    a `Camera` and allow import choose `Camera` asset type when publsihing, for
    `Geometry` choose `Geometry` and so on.
*   Publishing happens through the ftrack-python-api so no location plugins for
    the legacy api will be picked up. This also affects how things can be
    imported from the :term:`import dialog` since it is still using the legacy
    api. Longterm we will refactor the :term:`import dialog` to use the
    ftrack-python-api while providing a compatibility layer. For now
    publish/import workflow requires the Centralised storage scenario or another
    location that is available in both api clients.

Below is a list of limitations in regards to the Developer / TD aspect of the
tools that is likely to be solved before the final release:

*   There are limited support for modifying a bundled :term:`publish action`.
*   Validation :term:`pyblish plugin` are not yet supported.
*   The bundled :term:`pyblish plugin` are sourced by the
    :term:`ftrack-python-api` rather than when calling
    `pyblish.plugin.register_plugin_path`.
*   The current iteration of the :term:`Import dialog` cannot import published
    alembics.

Feedback
--------

Please add relevant feedback to the beta forum,
http://forum.ftrack.com/index.php?/forum/36-new-integrations, or contact
support@ftrack.com.
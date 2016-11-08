..
    :copyright: Copyright (c) 2016 ftrack

********
Glossary
********

.. glossary::

    asset plugin
        A python plugin that is responsible of publish, import and switching of
        an asset version.

        See :ref:`developing/asset_plugin` to learn more about how to develop
        your own plugin.

    ftrack Connect
        Integration of ftrack with other systems and the desktop. Provided by a
        core service that runs on each individuals machine and then separate
        integration plugins into a variety of third-party software.

        .. seealso::

            :ref:`ftrack Connect <ftrack-connect:about>`

    ftrack Connect package
        ftrack Connect package is a pre-built bundle of :term:`ftrack Connect`
        and the most commonly used :term:`ftrack Connect` plugins.

    ftrack-python-api
        A python client for the ftrack api. See
        http://ftrack-python-api.rtd.ftrack.com/en/stable/

    import dialog
        Used for importing assets into Maya, Nuke and other applications. Part
        of the current :term:`ftrack Connect package` integrations. 

    publish action
        An action registered by an :term:`asset plugin` that manages the publish
        of an asset version.

    publish dialog
        A dialog that shows a list of possible items to publish and necessary
        options.

    pyblish
        "Pyblish is a free, open-source (LGPL) framework written in Python that
        brings test-driven development to visual effects and triple-A game
        creation."

        -- Pyblish website.

        Please visit http://pyblish.com/ for more information.

    pyblish plugin
        A plugin to :term:`pyblish` used as part of publishing.

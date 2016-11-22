# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import maya.cmds as mc
import maya.mel as mm


registered_plugins = False


def register_pyblish_plugins():
    '''Register pyblish plugins.'''
    import ftrack_connect_pipeline.shared_pyblish_plugins

    ftrack_connect_pipeline.shared_pyblish_plugins.register()


def get_plugin_information():
    '''Return plugin information for maya.'''
    import ftrack_connect_maya_publish._version
    return {
        'application_id': 'maya',
        'plugin_version': ftrack_connect_maya_publish._version.__version__
    }


def open_publish():
    '''Open publish dialog.'''
    import ftrack_api

    session = ftrack_api.Session()
    session.event_hub.subscribe(
        'topic=ftrack.pipeline.get-plugin-information',
        lambda event: get_plugin_information()
    )

    import ftrack_connect_maya_publish
    ftrack_connect_maya_publish.register_assets(session)

    global registered_plugins
    if registered_plugins is False:
        register_pyblish_plugins()
        registered_plugins = True

    import ftrack_connect_pipeline.ui.publish_actions_dialog
    ftrack_connect_pipeline.ui.publish_actions_dialog.show(session)


def create_publish_menu():
    '''Create publish menu.'''
    gMainWindow = mm.eval('$temp1=$gMainWindow')
    menu_name = 'ftrack new'
    if mc.menu(menu_name, exists=True):
        mc.deleteUI(menu_name)

    menu = mc.menu(
        menu_name,
        parent=gMainWindow,
        tearOff=False,
        label=menu_name
    )

    mc.menuItem(
        parent=menu,
        label="Publish",
        stp="python",
        command=lambda x: open_publish()
    )


mc.evalDeferred("create_publish_menu()")

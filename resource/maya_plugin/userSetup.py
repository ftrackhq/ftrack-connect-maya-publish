# :coding: utf-8
# :copyright: Copyright (c) 2014 ftrack

import maya.cmds as mc
import maya.mel as mm


def open_publish():
    import ftrack_api

    session = ftrack_api.Session()
    import ftrack_connect_pipeline.ui.publish_actions_dialog
    ftrack_connect_pipeline.ui.publish_actions_dialog.show(session)

    def callback(event):
        from ftrack_connect_maya_publish import __version__
        return {
            'application_id': 'maya',
            'plugin_version': __version__
        }

    session.event_hub.subscribe(
        'topic=ftrack.pipeline.get-plugin-information',
        callback
    )


def create_publish_menu():
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

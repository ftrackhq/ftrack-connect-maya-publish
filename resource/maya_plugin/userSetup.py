import maya.cmds as mc
import maya.mel as mm


def open_publish():
    import ftrack_api

    session = ftrack_api.Session()
    import ftrack_connect_pipeline.ui.publish_actions_dialog
    ftrack_connect_pipeline.ui.publish_actions_dialog.show(session)


def create_publish_menu():
    gMainWindow = mm.eval('$temp1=$gMainWindow')
    menu_name = 'ftrack new'
    if mc.menu(menu_name, exists=True):
        mc.deleteUI(menu_name)

    efesto_menu = mc.menu(
        menu_name,
        parent=gMainWindow,
        tearOff=False,
        label=menu_name
    )

    mc.menuItem(
        parent=efesto_menu,
        label="Publish",
        stp="python",
        command=lambda x: open_publish()
    )


mc.evalDeferred("create_publish_menu()")

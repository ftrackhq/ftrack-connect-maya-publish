# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os

import maya.cmds as mc
import maya.mel as mm


def create_publish_menu():
    '''Create publish menu.'''
    import ftrack_connect_maya_publish.plugin
    import ftrack_connect_pipeline

    plugin = ftrack_connect_maya_publish.plugin.MayaPlugin(
        context_id=os.environ['FTRACK_CONTEXT_ID']
    )
    ftrack_connect_pipeline.register_plugin(plugin)

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
        label='Publish',
        stp='python',
        command=lambda x: plugin.open_publish()
    )

    mc.menuItem(
        parent=menu,
        label='Change Context',
        stp='python',
        command=lambda x: plugin.open_switch_context()
    )


mc.evalDeferred('create_publish_menu()')

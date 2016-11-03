import pyblish.api
import maya.cmds as mc


# Helper functions

def bake(camera):
    tmp_cam_components = mc.duplicate(camera, un=1, rc=1)
    if mc.nodeType(tmp_cam_components[0]) == 'transform':
        tmp_cam = tmp_cam_components[0]
    else:
        tmp_cam = mc.ls(tmp_cam_components, type='transform')[0]
    pConstraint = mc.parentConstraint(camera, tmp_cam)
    try:
        mc.parent(tmp_cam, world=True)
    except RuntimeError:
        # camera is already in world space
        pass

    mc.bakeResults(
        tmp_cam,
        simulation=True,
        t=(
            mc.playbackOptions(q=True, minTime=True),
            mc.playbackOptions(q=True, maxTime=True)
        ),
        sb=1,
        at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'],
        hi='below')

    mc.delete(pConstraint)
    camera = tmp_cam
    return camera


def cleanup_bake(camera):
    mc.delete(camera)


def lock_camera(camera):

    channels = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    camera_values = {}

    for channel in channels:
        channel_name = '{0}.{1}'.format(camera, channel)
        channel_value = mc.getAttr(channel_name, l=True)
        camera_values.setdefault(channel, channel_value)
        mc.setAttr(channel_name, l=True)

    return camera_values


def unlock_camera(camera, original_values):

    for channel, value in original_values.items():
        channel_name = '{0}.{1}'.format(camera, channel)
        mc.setAttr(channel_name, l=value)


# Instance plugins

class PreCameraExtract(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder - 0.1
    families = ['ftrack.maya.camera']

    def process(self, instance):
        camera_options = instance.context.data['options'].get(
            'camera_options', {}
        )

        bake_camera_option = camera_options.get('bake', False)
        lock_camera_option = camera_options.get('lock', False)

        camera = str(instance)
        locked_attrs = {}

        if bake_camera_option:
            camera = bake(camera)

        if lock_camera_option:
            locked_attrs = lock_camera(camera)

        mc.select(str(camera), replace=True)
        instance.data['camera'] = camera
        instance.data['locked_attrs'] = locked_attrs


class PostCameraExtract(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder + 0.1
    families = ['ftrack.maya.camera']

    def process(self, instance):
        camera_options = instance.context.data['options'].get(
            'camera_options', {}
        )

        bake_camera_option = camera_options.get('bake', False)
        lock_camera_option = camera_options.get('lock', False)

        camera = instance.data['camera']
        locked_attrs = instance.data['locked_attrs']

        if lock_camera_option:
            locked_attrs = unlock_camera(camera, locked_attrs)

        if bake_camera_option:
            camera = cleanup_bake(camera)


pyblish.api.register_plugin(PreCameraExtract)
pyblish.api.register_plugin(PostCameraExtract)

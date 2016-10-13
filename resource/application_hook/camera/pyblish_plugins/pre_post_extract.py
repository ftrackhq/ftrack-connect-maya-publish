import pyblish.api
import maya.cmds as mc


"""
     def publish(self, publish_data):
        '''Publish or raise exception if not valid.'''

        processors = {
            'maya.binary': MayaBinaryFileProcessor.process,
            'maya.alembic': AlembicProcessor.process
        }

        bake_camera = publish_data['options'].get('camera_bake', False)
        lock_camera = publish_data['options'].get('camera_lock', False)

        camera = self.get_camera()
        original_values = {}

        if bake_camera:
            camera = self.bake_camera(camera)

        if lock_camera:
            original_values = self.lock_camera(camera)

        results = {}
        for exporter in publish_data['item_options']:
            process = processors.get(exporter)
            if process:
                results[exporter] = process(
                    publish_data['item_options'][exporter]
                )

        if lock_camera:
            self.unlock_camera(camera, original_values)

        if bake_camera:
            self.cleanup_bake(camera)

        print results
"""


# Helper functions

def bake(camera):
    tmpCamComponents = mc.duplicate(camera, un=1, rc=1)
    if mc.nodeType(tmpCamComponents[0]) == 'transform':
        tmpCam = tmpCamComponents[0]
    else:
        tmpCam = mc.ls(tmpCamComponents, type='transform')[0]
    pConstraint = mc.parentConstraint(camera, tmpCam)
    try:
        mc.parent(tmpCam, world=True)
    except RuntimeError:
        print 'camera already in world space'

    mc.bakeResults(
        tmpCam,
        simulation=True,
        t=(
            mc.playbackOptions(q=True, minTime=True),
            mc.playbackOptions(q=True, maxTime=True)
        ),
        sb=1,
        at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'],
        hi='below')

    mc.delete(pConstraint)
    camera = tmpCam
    return camera


def cleanup_bake(camera):
    mc.delete(camera)


def lock_camera(camera):
    channels = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    camera_values = {}
    print 'locking camera:', camera

    for channel in channels:
        channel_name = '{0}.{1}'.format(camera, channel)
        channel_value = mc.getAttr(channel_name, l=True)

        print 'getting : %s:%s' % (channel_name, channel_value)

        camera_values.setdefault(channel, channel_value)
        print "setting value to : %s" % channel_name
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
        camera_options = instance.context.data['options']['cam_options']
        bake_camera = camera_options['bake']
        lock_camera = camera_options['lock']

        camera = str(instance)
        locked_attrs = {}

        if bake_camera:
            print 'PRE PROCESSING CAMERA BAKE'
            camera = bake(camera)
            print 'PRE PROCESSING CAMERA BAKE DONE'

        if lock_camera:
            print 'PRE PROCESSING CAMERA LOCK'
            locked_attrs = lock_camera(camera)
            print 'PRE PROCESSING CAMERA LOCK DONE'

        instance.data['camera'] = camera
        instance.data['locked_attrs'] = locked_attrs


class PostCameraExtract(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder + 0.1
    families = ['ftrack.maya.camera']

    def process(self, instance):
        camera_options = instance.context.data['options']['cam_options']
        bake_camera = camera_options['bake']
        lock_camera = camera_options['lock']

        camera = instance.data['camera']
        locked_attrs = instance.data['locked_attrs']

        if lock_camera:
            print 'POST PROCESSING CAMERA LOCK'
            locked_attrs = unlock_camera(camera, locked_attrs)
            print 'POST PROCESSING CAMERA LOCK DONE'

        if bake_camera:
            print 'POST PROCESSING CAMERA BAKE'
            camera = cleanup_bake(camera) 
            print 'POST PROCESSING CAMERA BAKE DONE'



pyblish.api.register_plugin(PreCameraExtract)
pyblish.api.register_plugin(PostCameraExtract)

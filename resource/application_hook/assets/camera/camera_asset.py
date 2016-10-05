import tempfile

import ftrack_api

import ftrack_connect_pipeline.asset
from ftrack_connect_pipeline.ui.widget.field.base import BaseField

from PySide import QtGui
import maya.cmds as mc


IDENTIFIER = 'camera'

# MAYA AND ALEMBIC PROCESSOR CLASSES


class MayaBinaryFileProcessor(object):

    @staticmethod
    def options():
        return [
            {
                'type': 'boolean',
                'label': 'Preserve reference',
                'name': 'reference',
                'value': False
            },
            {
                'type': 'boolean',
                'label': 'History',
                'name': 'history',
                'value': False
            },
            {
                'type': 'boolean',
                'label': 'Channels',
                'name': 'channels',
                'value': False
            },
            {
                'type': 'boolean',
                'label': 'Expressions',
                'name': 'expressions',
                'value': False
            },
            {
                'type': 'boolean',
                'label': 'Constraints',
                'name': 'constraint',
                'value': False
            },
            {
                'type': 'boolean',
                'label': 'Shaders',
                'name': 'shaders',
                'value': True
            },
            {
                'type': 'boolean',
                'label': 'Export Selected',
                'name': 'export_selected',
                'value': False
            }
        ]

    @staticmethod
    def process(options):

        import tempfile
        # generate temp file
        temporaryPath = tempfile.mkstemp(suffix='.mb')[-1]

        export_selected = options.get('export_selected', False)
        # save maya file
        mc.file(
            temporaryPath,
            op='v=0',
            typ='mayaBinary',
            preserveReferences=options.get('reference', False),
            constructionHistory=options.get('keep_history', False),
            channels=options.get('keep_channels', False),
            constraints=options.get('keep_constraints', False),
            expressions=options.get('keep_expressions', False),
            shader=options.get('keep_shaders', False),
            exportSelected=export_selected,
            exportAll=not export_selected,
            force=True
        )

        return temporaryPath


class AlembicProcessor(object):

    @staticmethod
    def options():
        return [
            {
                'type': 'boolean',
                'label': 'Include animation',
                'name': 'animation',
                'value': False

            },
            {
                'type': 'boolean',
                'label': 'UV Write',
                'name': 'uv_write',
                'value': True
            },
            {
                'widget': StartEndFrameFields(),
                'label': 'start/end frame',
                'type': 'qt_widget',
                'name': 'frame_range'
            },
            {
                'type': 'boolean',
                'label': 'World Space',
                'name': 'world_space',
                'value': True,
            },
            {
                'type': 'boolean',
                'label': 'Write Visibility',
                'name': 'write_visibility',
                'value': True,

            },
            {
                'type': 'qt_widget',
                'label': 'Evaluate Every',
                'name': 'sampling',
                'widget': SamplingField()
            },
            {
                'type': 'boolean',
                'label': 'Export Selected',
                'name': 'export_selected',
                'value': False
            }
        ]

    @staticmethod
    def process(options):

        # export alembic file
        temporaryPath = tempfile.mkstemp(suffix='.abc')[-1]

        if options.get('export_selected', False):
            nodes = mc.ls(sl=True, long=True)
            selectednodes = None
        else:
            selectednodes = mc.ls(sl=True, long=True)
            nodes = mc.ls(type='transform', long=True)

        objCommand = ''
        for n in nodes:
            objCommand = objCommand + '-root ' + n + ' '

        alembicJobArgs = ''

        if options.get('uv_write', False):
            alembicJobArgs += '-uvWrite '

        if options.get('world_space', False):
            alembicJobArgs += '-worldSpace '

        if options.get('write_visibility', False):
            alembicJobArgs += '-writeVisibility '

        if options.get('animation', False):
            alembicJobArgs += '-frameRange {0} {1} -step {2} '.format(
                options['frame_range'].get('start_frame', 0),
                options['frame_range'].get('end_frame', 0),
                options['sampling'].get('sampling', 1)
            )

        mc.loadPlugin('AbcExport.so', qt=1)

        alembicJobArgs += ' ' + objCommand + '-file ' + temporaryPath
        mc.AbcExport(j=alembicJobArgs)

        if selectednodes:
            mc.select(selectednodes)

        return temporaryPath

# CUSTOM WIDGETS


class StartEndFrameFields(BaseField):

    def __init__(self):
        super(StartEndFrameFields, self).__init__()
        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self.start_f = QtGui.QDoubleSpinBox()
        self.start_f.setValue(mc.playbackOptions(q=True, minTime=True))

        self.end_f = QtGui.QDoubleSpinBox()
        self.end_f.setValue(mc.playbackOptions(q=True, maxTime=True))

        self.layout().addWidget(self.start_f)
        self.layout().addWidget(self.end_f)

    def notify_changed(self, *args, **kwargs):
        '''Notify the world about the changes.'''
        self.value_changed.emit(self.value())

    def value(self):
        return {
            'start_frame': self.start_f.value(),
            'end_frame': self.end_f.value()
        }


class SamplingField(BaseField):

    def __init__(self):
        super(SamplingField, self).__init__()
        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self.samples = QtGui.QDoubleSpinBox()
        self.samples.setValue(0.1)

        self.layout().addWidget(self.samples)

    def notify_changed(self, *args, **kwargs):
        '''Notify the world about the changes.'''
        self.value_changed.emit(self.value())

    def value(self):
        return {
            'samples': self.samples.value(),
        }


# ACTUAL PUBLISHER


class PublishCamera(ftrack_connect_pipeline.asset.PublishAsset):
    '''Handle publish of maya camera.'''

    def get_options(self, publish_data):
        options = [
            {
                'type': 'boolean',
                'label': 'Bake Camera',
                'name': 'camera_bake',
                'value': True

            },
            {
                'type': 'boolean',
                'label': 'Lock Camera',
                'name': 'camera_lock',
                'value': True
            }
        ]
        default_options = super(PublishCamera, self).get_options(publish_data)
        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = [
            {
                'type': 'boolean',
                'label': 'Publish Maya Binary',
                'name': 'maya.binary',
            },
            {
                'type': 'boolean',
                'label': 'Publish Alembic',
                'name': 'maya.alembic'
            }
        ]
        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''

        options = {
            'maya.binary': MayaBinaryFileProcessor.options(),
            'maya.alembic': AlembicProcessor.options()
        }

        return options.get(name, [])

    def get_camera(self):
        # Get original selection
        nodes = mc.ls(sl=True)

        # Get camera shape and parent transforms
        cameraShape = ''
        for node in nodes:
            if mc.nodeType(node) == 'camera':
                cameraShape = node
            else:
                cameraShapes = mc.listRelatives(
                    node, allDescendents=True, type='camera'
                )
                if len(cameraShapes) > 0:
                    # We only care about one camera
                    cameraShape = cameraShapes[0]

        if cameraShape == '':
            raise Exception('No Camera Selected')

        cameraTransform = mc.listRelatives(
            cameraShape, type='transform', parent=True
        )
        cameraTransform = cameraTransform[0]
        return cameraTransform

    def bake_camera(self, camera):
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

    def cleanup_bake(self, camera):
        mc.delete(camera)

    def lock_camera(self, camera):
        channels = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        camera_values = {}
        for channel in channels:
            channel_name = '{0}.{1}'.format(camera, channel)
            camera_values.setdefault(channel, mc.getAttr(channel_name, l=True))
            mc.setAttr(channel_name, l=True)

        return camera_values

    def unlock_camera(self, camera, original_values):
        for channel, value in original_values.items():
            channel_name = '{0}.{1}'.format(camera, channel)
            mc.setAttr(channel_name, l=value)

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


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    geo_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishCamera(
            label=IDENTIFIER,
            description='publish camera to ftrack.',
            icon='http://www.clipartbest.com/cliparts/LiK/dLB/LiKdLB6zT.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    geo_asset.register(session)

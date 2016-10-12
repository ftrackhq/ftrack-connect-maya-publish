import ftrack_api

import ftrack_connect_pipeline.asset
IDENTIFIER = 'camera'

from ftrack_connect_pipeline.ui.widget.field.base import BaseField
from PySide import QtGui


# TEMP SOLUTION WHILE WAITING TO BUILD OPTIONS OUT OF DICTS
class MayaBinaryOptions(BaseField):

    def __init__(self):
        super(MayaBinaryOptions, self).__init__()
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        # preserve reference
        self.preserve_reference = QtGui.QCheckBox('preserve reference')
        self.layout().addWidget(self.preserve_reference)

        self.history = QtGui.QCheckBox('history')
        self.layout().addWidget(self.history)

        self.channels = QtGui.QCheckBox('channels')
        self.layout().addWidget(self.channels)

        self.expressions = QtGui.QCheckBox('expressions')
        self.layout().addWidget(self.expressions)

        self.constraints = QtGui.QCheckBox('constraints')
        self.layout().addWidget(self.constraints)

        self.shaders = QtGui.QCheckBox('shaders')
        self.layout().addWidget(self.shaders)

        self.export_selected = QtGui.QCheckBox('export_selected')
        self.layout().addWidget(self.export_selected)

        self.preserve_reference.stateChanged.connect(self.notify_changed)
        self.history.stateChanged.connect(self.notify_changed)
        self.channels.stateChanged.connect(self.notify_changed)
        self.expressions.stateChanged.connect(self.notify_changed)
        self.constraints.stateChanged.connect(self.notify_changed)
        self.shaders.stateChanged.connect(self.notify_changed)
        self.export_selected.stateChanged.connect(self.notify_changed)

    def notify_changed(self, *args, **kwargs):
        '''Notify the world about the changes.'''
        self.value_changed.emit(self.value())

    def value(self):
        return {
            'reference': self.preserve_reference.checkState(),
            'history': self.history.checkState(),
            'channels': self.channels.checkState(),
            'expressions': self.expressions.checkState(),
            'constraints': self.constraints.checkState(),
            'shaders': self.shaders.checkState(),
            'export_selected': self.export_selected.checkState()
        }


# NOTE THIS LACK OF TWO FILEDS, AS SOON AS I CAN BUILD OUT OF THE DICT I'LL BE UPDATING THIS
# BEING THIS A GEOMETRY, ANIMATION MIGHT NOT BE NEEDED THOUGH, AND SHOULD GO IN A CACHE ASSET TYPE

class AlembicOptions(BaseField):

    def __init__(self):
        super(AlembicOptions, self).__init__()
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        # preserve reference
        self.include_animation = QtGui.QCheckBox('include animation')
        self.layout().addWidget(self.include_animation)

        self.uv_write = QtGui.QCheckBox('Write UV')
        self.layout().addWidget(self.uv_write)

        self.world_space = QtGui.QCheckBox('World Space')
        self.layout().addWidget(self.world_space)

        self.write_visibility = QtGui.QCheckBox('Write Visibility')
        self.layout().addWidget(self.write_visibility)

        self.include_animation.stateChanged.connect(self.notify_changed)
        self.uv_write.stateChanged.connect(self.notify_changed)
        self.world_space.stateChanged.connect(self.notify_changed)
        self.write_visibility.stateChanged.connect(self.notify_changed)

    def notify_changed(self, *args, **kwargs):
        '''Notify the world about the changes.'''
        self.value_changed.emit(self.value())

    def value(self):
        return {
            'include_animation': self.include_animation.checkState(),
            'uv_write': self.uv_write.checkState(),
            'world_space': self.world_space.checkState(),
            'write_visibility': self.write_visibility.checkState()
        }


class CameraOptions(BaseField):

    def __init__(self):
        super(CameraOptions, self).__init__()
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        # preserve reference
        self.bake = QtGui.QCheckBox('Bake')
        self.layout().addWidget(self.bake)

        self.lock = QtGui.QCheckBox('Lock')
        self.layout().addWidget(self.lock)

        self.bake.stateChanged.connect(self.notify_changed)
        self.lock.stateChanged.connect(self.notify_changed)

    def notify_changed(self, *args, **kwargs):
        '''Notify the world about the changes.'''
        self.value_changed.emit(self.value())

    def value(self):
        return {
            'bake': self.bake.checkState(),
            'lock': self.lock.checkState()
        }


class PublishCamera(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya image.'''

    def get_options(self, publish_data):
        options = [
            {
                'type': 'qt_widget',
                'label': 'Maya Binary Options',
                'name': 'mb_options',
                'widget': MayaBinaryOptions()
            },
            {
                'type': 'qt_widget',
                'label': 'Alembic Options',
                'name': 'abc_options',
                'widget': AlembicOptions()
            },
            {
                'type': 'qt_widget',
                'label': 'Camera Options',
                'name': 'cam_options',
                'widget': CameraOptions()
            },
        ]

        default_options = super(
            PublishCamera, self
        ).get_options(publish_data)

        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.maya.camera',):
                options.append(
                    {
                        'label': instance.name,
                        'name': instance.id,
                        'value': True
                    }
                )

        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''
        return []


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishCamera(
            label='Camera',
            description='publish camera to ftrack.',
            icon='http://www.clipartbest.com/cliparts/LiK/dLB/LiKdLB6zT.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)

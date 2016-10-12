import ftrack_api

import ftrack_connect_pipeline.asset
IDENTIFIER = 'geometry'

from ftrack_connect_pipeline.ui.widget.field.base import BaseField
from PySide import QtGui
import maya.cmds as cmds


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

    def notify_changed(self, *args, **kwargs):
        '''Notify the world about the changes.'''
        self.value_changed.emit(self.value())

    def value(self):
        return {
            'reference': self.preserve_reference.checked(),
            'history': self.history.checked(),
            'channels': self.channels.checked(),
            'expressions': self.expressions.checked(),
            'constraints': self.constraints.checked(),
            'shaders': self.shaders.checked(),
            'export_selected': self.export_selected.checked(),
        }


# NOTE THIS LACK OF TWO FILEDS, AS SOON AS I CAN BUILD OUT OF THE DICT I'LL BE UPDATING THIS
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

    def notify_changed(self, *args, **kwargs):
        '''Notify the world about the changes.'''
        self.value_changed.emit(self.value())

    def value(self):
        return {
            'include_animation': self.include_animation.checked(),
            'uv_write': self.uv_write.checked(),
            'world_space': self.world_space.checked(),
            'write_visibility': self.write_visibility.checked(),
        }


class PublishGeometry(ftrack_connect_pipeline.asset.PyblishAsset):
    '''Handle publish of maya image.'''

    def get_options(self, publish_data):
        options = [
            {
                'type': 'qt_widget',
                'label': 'MayaBinaryOptions',
                'name': 'mboptions',
                'widget': MayaBinaryOptions()
            },
            {
                'type': 'qt_widget',
                'label': 'AlembicOptions',
                'name': 'abcoptions',
                'widget': AlembicOptions()
            },
        ]

        default_options = super(PublishGeometry, self).get_options(publish_data)
        options += default_options
        return options

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = []
        for instance in publish_data:
            if instance.data['family'] in ('ftrack.maya.geometry', ):
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
        for instance in publish_data:
            if instance.id == name:
                return []

        return []


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishGeometry(
            label='Geometry',
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)

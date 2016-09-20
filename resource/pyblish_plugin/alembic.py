import pyblish.api
import maya.cmds as mc
import tempfile

from PySide import QtCore, QtGui


# class FrameRangeWidget(QtGui.QWidget):

#     values_changed = QtCore.Signal(object)

#     def __init__(self, parent=None):
#         super(FrameRangeWidget, self).__init__(parent=parent)
#         layout = QtGui.QHBoxLayout()
#         self.setLayout(layout)

#         m_start_frame = mc.playbackOptions(q=True, minTime=True)
#         m_end_frame = mc.playbackOptions(q=True, maxTime=True)

#         self._start_frame = QtGui.QDoubleSpinBox()
#         self._end_frame = QtGui.QDoubleSpinBox()

#         self._start_frame.setValue(m_start_frame)
#         self._end_frame.setValue(m_end_frame)

#         layout.addWidget(self._start_frame)
#         layout.addWidget(self._end_frame)

#         self._start_frame.valueChanged.connect(
#             self.notify_changed
#         )

#         self._end_frame.valueChanged.connect(
#             self.notify_changed
#         )

#     def notify_changed(self, *args, **kwargs):
#         '''Notify the world about the changes.'''
#         self.values_changed.emit(self.value())

#     def value(self):
#         '''Return value.'''
#         start_frame = self._start_frame.value()
#         end_frame = self._end_frame.value()

#         return {
#             'start_frame': start_frame,
#             'end_frame': end_frame,
#         }


class CollecAlembic(pyblish.api.ContextPlugin):
    '''Collect nuke write nodes fr`om scene.'''
    name = 'Publish write node content'
    order = pyblish.api.CollectorOrder

    # @classmethod
    # def _ftrack_options(cls, context):
    #     '''Return options.'''
    #     frame_range = FrameRangeWidget()

    #     def handle_change(value):
    #         context.data['options'] = {}
    #         context.data['options']['start_frame'] = value['start_frame']
    #         context.data['options']['end_frame'] = value['end_frame']

    #     frame_range.values_changed.connect(handle_change)

    #     return frame_range

    def process(self, context):
        '''Process *context* and add maya camera instances.'''

        instance = context.create_instance(
            'alembic', family='ftrack.maya.alembic'
        )

        instance.data['publish'] = True

        instance.data['options'] = {
            'animation': False,
            'uv_write': True,
            'world_space': True,
            'write_visibility': True,
            'sampling': 1.00,
            'start_frame': mc.playbackOptions(q=True, minTime=True),
            'end_frame': mc.playbackOptions(q=True, maxTime=True)
        }
        instance.data['ftrack_components'] = []


class ExtractAlembicScene(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder
    families = ['ftrack.maya.alembic']

    @classmethod
    def _ftrack_options(cls, instance):

        '''Return options.'''
        return [
            {
                'type': 'boolean',
                'label': 'Include animation',
                'name': 'animation'
            },
            {
                'type': 'boolean',
                'label': 'UV Write',
                'name': 'uv_write'
            },
            {
                'type': 'text',
                'label': 'Start Frame',
                'name': 'start_frame'
            },
            {
                'type': 'text',
                'label': 'End Frame',
                'name': 'end_frame'
            },
            {
                'type': 'boolean',
                'label': 'World Space',
                'name': 'world_space'
            },
            {
                'type': 'boolean',
                'label': 'Write Visibility',
                'name': 'write_visibility'
            },
            {
                'type': 'text',
                'label': 'Evaluate Every',
                'name': 'sampling'
            },
            {
                'type': 'boolean',
                'label': 'Export Selected',
                'name': 'export_selected'
            }
        ]

    def process(self, instance):
        '''Process *instance* and extract media.'''
        if instance.data.get('publish'):
            print (
                'Extracting media using options:',
                instance.data.get('options')
            )

            # extract options
            keep_reference = instance.data['options']['reference']
            keep_history = instance.data['options']['history']
            keep_channels = instance.data['options']['channels']
            keep_constraints = instance.data['options']['constraint']
            keep_expressions = instance.data['options']['expressions']
            keep_shaders = instance.data['options']['shaders']
            attach_scene = instance.data['options']['attach_scene']
            export_selected = instance.data['options']['export_selected']

            temporaryPath = tempfile.NamedTemporaryFile(
                suffix='.mb', delete=False
            ).name

            # generate temp file
            mc.file(
                temporaryPath,
                op='v=0',
                typ='mayaBinary',
                preserveReferences=keep_reference,
                constructionHistory=keep_history,
                channels=keep_channels,
                constraints=keep_constraints,
                expressions=keep_expressions,
                shader=keep_shaders,
                exportSelected=export_selected,
                exportAll=attach_scene,
                force=True
            )

            instance.data['ftrack_components'].append(
                {
                    'name': instance.name,
                    'path': temporaryPath,
                }
            )


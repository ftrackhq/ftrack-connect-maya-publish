import tempfile

import ftrack_api

import ftrack_connect_pipeline.asset
from ftrack_connect_pipeline.ui.widget.field.base import BaseField

from PySide import QtGui
import maya.cmds as mc


IDENTIFIER = 'rig'

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


class PublishRig(ftrack_connect_pipeline.asset.PublishAsset):
    '''Handle publish of maya geometry.'''

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = [
            {
                'type': 'boolean',
                'label': 'Publish Maya Binary',
                'name': 'maya.binary'
            }
        ]
        return options

    def get_item_options(self, publish_data, name):
        '''Return options for publishable item with *name*.'''

        options = {
            'maya.binary': MayaBinaryFileProcessor.options(),
        }

        return options.get(name, [])

    def publish(self, publish_data):
        '''Publish or raise exception if not valid.'''
        processors = {
            'maya.binary': MayaBinaryFileProcessor.process,
        }
        results = {}
        for exporter in publish_data['item_options']:
            process = processors.get(exporter)
            if process:
                results[exporter] = process(
                    publish_data['item_options'][exporter]
                )

        print results


def register(session):
    '''Subscribe to *session*.'''
    if not isinstance(session, ftrack_api.Session):
        return

    geo_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishRig(
            label=IDENTIFIER,
            description='publish rig to ftrack.',
            icon='http://www.clipartbest.com/cliparts/xig/onp/xigonpB5T.gif'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    geo_asset.register(session)

import ftrack_api

import ftrack_connect_pipeline.asset

import tempfile
import maya.cmds as mc

IDENTIFIER = 'geometry'


class PublishGeometry(ftrack_connect_pipeline.asset.PublishAsset):
    '''Handle publish of maya geometry.'''

    def get_publish_items(self, publish_data):
        '''Return list of items that can be published.'''
        options = [
            {
                'type': 'boolean',
                'label': 'Publish Maya Binary',
                'name': 'maya.binary'
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
            'maya.binary': [
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
            ],
            'maya.alembic': [
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
                    'type': 'text',
                    'label': 'Start Frame',
                    'name': 'start_frame',
                    'value': mc.playbackOptions(q=True, minTime=True)
                },
                {
                    'type': 'text',
                    'label': 'End Frame',
                    'name': 'end_frame',
                    'value': mc.playbackOptions(q=True, maxTime=True)
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
                    'type': 'text',
                    'label': 'Evaluate Every',
                    'name': 'sampling',
                    'value': 0.1
                },
                {
                    'type': 'boolean',
                    'label': 'Export Selected',
                    'name': 'export_selected',
                    'value': False
                }
            ]
        }

        return options.get(name, [])

    def _process_mayabinary(self, options):
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

    def _process_alembic(self, options):

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
                options.get('start_frame', 0),
                options.get('end_frame', 0),
                options.get('sampling', 1)
            )

        mc.loadPlugin('AbcExport.so', qt=1)

        alembicJobArgs += ' ' + objCommand + '-file ' + temporaryPath
        mc.AbcExport(j=alembicJobArgs)

        if selectednodes:
            mc.select(selectednodes)

        return temporaryPath

    def publish(self, publish_data):
        '''Publish or raise exception if not valid.'''
        processors = {
            'maya.binary': self._process_mayabinary,
            'maya.alembic': self._process_alembic
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

    image_asset = ftrack_connect_pipeline.asset.Asset(
        identifier=IDENTIFIER,
        publish_asset=PublishGeometry(
            label=IDENTIFIER,
            description='publish geometry to ftrack.',
            icon='http://www.clipartbest.com/cliparts/9Tp/erx/9Tperxqrc.png'
        )
    )
    # Register media asset on session. This makes sure that discover is called
    # for import and publish.
    image_asset.register(session)

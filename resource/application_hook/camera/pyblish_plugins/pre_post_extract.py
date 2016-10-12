import pyblish.api


class PreCameraBakeExtract(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder - 0.2
    families = ['ftrack.maya.mayabinary', 'ftrack.maya.alembic']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        print 'Running pre Bake'
        pass


class PreCameraLockExtract(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder - 0.1
    families = ['ftrack.maya.mayabinary', 'ftrack.maya.alembic']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        print 'Running pre Lock'
        pass


class PostCameraLockExtract(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder + 0.1
    families = ['ftrack.maya.mayabinary', 'ftrack.maya.alembic']

    def process(self, instance):
        '''Process *instance* and extract media.'''
        print 'Running post Lock'
        pass


class PostCameraBakeExtract(pyblish.api.InstancePlugin):
    '''prepare component to be published'''
    order = pyblish.api.ExtractorOrder + 0.2
    families = ['ftrack.maya.mayabinary', 'ftrack.maya.alembic']

    def process(self, instance):
        print 'Running post Bake'
        '''Process *instance* and extract media.'''
        pass

..
    :copyright: Copyright (c) 2016 ftrack

.. _installation:

************
Installation
************

.. note::

    The installation process is manual and requires basic understanding of Git,
    Terminal and Python. Future releases will be automatic.

Installation guide
==================

#.  Open a terminal and navigate to a <connect-plugin-directory. The directory
    can be found from Connect menu > Open plugin directory.
#.  git clone git@bitbucket.org:ftrack/ftrack-connect-maya-publish.git to
    <connect-plugin-directory>.
#.  cd to <connect-plugin-directory>/ftrack-connect-maya-publish/
#.  Install all dependencies to a ftrack-connect-maya-publish into a directory
    with::

        pip install --target=dependencies --verbose --upgrade --process-dependency-links .

#.  This is all good if you want to try things out. But if we want to use the
    source rather than the installed ftrack_connect_maya_publish package you
    will need to remove it::

        rm -r dependencies/ftrack_connect_maya_publish
        rm -r dependencies/ftrack_connect_maya_publish-VERSION-py2.7.egg-info

Usage
=====

#.  Start ftrack Connect (close and start if already running).
#.  Start Maya for a task using ftrack connect or the ftrack web UI.
#.  Open menu `ftrack new` and choose one of the publish actions.

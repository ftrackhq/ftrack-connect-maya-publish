..
    :copyright: Copyright (c) 2016 ftrack

.. _installation:

************
Installation
************

.. note::

    The installation process is technical at the moment and the current
    iteration requires basic technical understanding of Git, Terminal and Python.
    Future itrations will of course be much more userfriendly in this regard.

Installation guide
==================

#.  git clone git@bitbucket.org:ftrack/ftrack-connect-maya-publish.git to
    <connect-plugin-directory>.
#.  cd to <connect-plugin-directory>/ftrack-connect-maya-publish/
#.  Install all dependencies to a ftrack-connect-maya-publish into a directory
    with::

        pip install --target=dependencies --verbose --upgrade --process-dependency-links .

Usage
=====

#.  Start ftrack Connect (close and start if already running).
#.  Start Maya on a task.
#.  Open menu `ftrack new` and choose one of the publish actions.

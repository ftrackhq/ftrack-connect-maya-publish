###############################
ftrack-connect-maya-publish
###############################

This repository contains a publish dialog for Maya. It is meant to be used as a
Connect plugin.

*************
Documentation
*************

Installation guide
==================

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
#.  Start Maya on a task.
#.  Create a write node and render material.
#.  Open menu `ftrack new` and choose Media.
#.  Fill out form and try to publish.

*********************
Copyright and license
*********************

Copyright (c) 2016 ftrack

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License in the LICENSE.txt file, or at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.


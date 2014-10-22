# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014, Craig Tracey
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations

import uuid

DEFAULT_IMAGE = 'ubuntu-12.04'
DEFAULT_FLAVOR = 'm1.medium'
DEFAULT_USER = 'ubuntu'
DEFAULT_KEY_NAME = 'dagobah'
DEFAULT_PACKER_URL = 'https://dl.bintray.com/mitchellh/packer/0.6.1_linux_amd64.zip'  # noqa


class BuildInstanceSettings(object):

    def __init__(self, settings):
        self._settings = settings.get('build_instance', {})
        self.name = self._settings.get('name', 'imgcreator-%s' % uuid.uuid4())
        self.image = self._settings.get('image', DEFAULT_IMAGE)
        self.flavor = self._settings.get('flavor', DEFAULT_FLAVOR)
        self.user = self._settings.get('user', DEFAULT_USER)
        self.key_name = self._settings.get('key_name', DEFAULT_KEY_NAME)
        self.net_id = self._settings.get('net_id', None)
        self.packer_url = self._settings.get('packer_url', DEFAULT_PACKER_URL)

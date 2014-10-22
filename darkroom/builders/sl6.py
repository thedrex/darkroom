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

from darkroom.image_builder import ImageBuilder
from darkroom.packer_settings import PackerSettings

DISTRO_ISO_INFO = {
    'scientific': {
        '6.5': {
#            'iso_url': 'http://mirror.mcs.anl.gov/pub/scientific-linux/6.5/x86_64/iso/SL-65-x86_64-2014-01-27-Install-DVD.iso',  # noqa
            'iso_url': 'http://drewsnest.com/SL-65-x86_64-2014-01-27-Install-DVD.iso',  # noqa
            'iso_checksum': 'a95e182f6ed14a4fb36e448d6eb19a6a59a34778',
            'iso_checksum_type': 'sha1'
        }
    }
}


DEFAULT_BOOT_COMMAND = ["<tab> text ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/kickstart.cfg<enter>"]  # noqa


class SLImageBuilder(ImageBuilder):

    def __init__(self, settings):
        self._settings = settings
        self.name = settings.get('name', None)
        self.distro = settings.get('distro', None)
        self.version = settings.get('version', None)
        self.kickstart_path = settings.get('kickstart_path', None)
        self.boot_command = DEFAULT_BOOT_COMMAND
        self._packer_settings = None
        super(SLImageBuilder, self).__init__(settings)

    @staticmethod
    def supported_distros():
        return DISTRO_ISO_INFO.keys()

    def _get_packer_settings(self):
        if not self._packer_settings:
            image_info = DISTRO_ISO_INFO[self.distro][self.version]
            image_info['name'] = self.name
            image_info['boot_command'] = self.boot_command
            self._packer_settings = PackerSettings(**image_info)
        return self._packer_settings

    def get_packer_config(self):
        packer_settings = self._get_packer_settings()
        return packer_settings.get_config()

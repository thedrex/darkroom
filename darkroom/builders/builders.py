from darkroom.image_builder import ImageBuilder
from darkroom.packer_settings import PackerSettings

DISTRO_ISO_INFO = {
    'scientific': {
        '6.5': {
            'iso_url': 'http://mirrors.200p-sf.sonic.net/scientific/6.5/x86_64/iso/SL-65-x86_64-2013-12-05-boot.iso',  # noqa
            'iso_checksum': '2c56df9b6a6cce14fae802de0bb4a675b5bdc69d',
            'iso_checksum_type': 'sha1'
        }
    },
    'centos': {
        '5.11': {
            'iso_url': 'http://mirror.raystedman.net/centos/5/isos/x86_64/CentOS-5.11-x86_64-netinstall.iso',  # noqa
            'iso_checksum': 'f2087f9af0d50df05144a1f0d1c5b404',
            'iso_checksum_type': 'md5'
        }
    }

}


DEFAULT_BOOT_COMMAND = ["<tab> cmdline ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/kickstart.cfg selinux=0<enter>"]  # noqa


class LinuxImageBuilder(ImageBuilder):

    def __init__(self, settings):
        self._settings = settings
        self.name = settings.get('name', None)
        self.distro = settings.get('distro', None)
        self.version = settings.get('version', None)
        self.kickstart_path = settings.get('kickstart_path', None)
        self.boot_command = DEFAULT_BOOT_COMMAND
        self._packer_settings = None
        super(LinuxImageBuilder, self).__init__(settings)

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

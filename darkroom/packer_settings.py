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

import json

PACKER_BUILDER_BASE = {
    "builders": [
        {
            "type": "qemu",
            "output_directory": "packer_output",
            "shutdown_command": "halt -p",
            "disk_size": 10000,
            "format": "qcow2",
            "headless": True,
            "accelerator": "kvm",
            "http_directory": "httpdir",
            "http_port_min": 10082,
            "http_port_max": 10089,
            "ssh_host_port_min": 2222,
            "ssh_host_port_max": 2229,
            "ssh_username": "root",
            "ssh_password": "s0m3pass",
            "ssh_port": 22,
            "ssh_wait_timeout": "90m",
            "net_device": "virtio-net",
            "disk_interface": "virtio",
            "boot_wait": "10s",
            "qemuargs": [
                ["-m", "2048m"]
#                ["-smp", "4"]
            ],
            "boot_command": [
                "<tab> linux text ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/kickstart.cfg ip=dhcp dns=8.8.8.8<enter>"  # noqa
            ]
        }
    ],
    "provisioners": [
        {
            "type": "shell",
            "inline": [
                "passwd --delete root",
                "sed -i 's/PermitRootLogin.*/PermitRootLogin without-password/g;' /etc/ssh/sshd_config"  # noqa
            ]
        }
    ]
}


class PackerSettings(object):

    def __init__(self, name, iso_url, iso_checksum, iso_checksum_type,
                 disk_size=10000, ssh_password=None, boot_command=None):
        self.vm_name = name
        self.iso_url = iso_url
        self.iso_checksum = iso_checksum
        self.iso_checksum_type = iso_checksum_type
        self.disk_size = disk_size
        self.ssh_password = ssh_password
        self.boot_command = boot_command
        self._config = None

    def get_config(self):
        if not self._config:
            custom_keys = {}
            for key in ('vm_name', 'iso_url', 'iso_checksum',
                        'iso_checksum_type', 'disk_size', 'ssh_password',
                        'boot_command'):
                val = getattr(self, key)
                if val:
                    custom_keys[key] = val
            config = PACKER_BUILDER_BASE
            config['builders'][0].update(custom_keys)
            self._config = json.dumps(config, sort_keys=True, indent=4,
                                      separators=(',', ': '))
        return self._config

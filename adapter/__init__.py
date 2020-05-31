# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>

"""AwoxMeshLight adapter for Mozilla WebThings Gateway."""

import os

from awoxmeshlight import AwoxMeshLight
from gateway_addon import Adapter, Database
from .device import AwoxMeshLightDevice


class AwoxMeshLightAdapter(Adapter):
    """Adapter for Awox Mesh Light"""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """

        self.pairing = False
        self.addon_name = 'awox-mesh-light'
        self.DEBUG = False
        self.name = self.__class__.__name__
        self.URL = 'https://github.com/rzr/awox-mesh-light-webthing'
        Adapter.__init__(self,
                         self.addon_name, self.addon_name, verbose=verbose)

        try:
            self._add_from_config()

        except Exception as ex:
            print("error: Could not create awox_mesh_light_device: " + str(ex))


    def _add_from_config(self):
        """Attempt to add all configured devices."""
        database = Database('awox-mesh-light-adapter')
        if not database.open():
            return

        config = database.load_config()
        database.close()

        if not config or 'address' not in config:
            return
        try:
            self.DEBUG and print(config['address'])
            self.controller = AwoxMeshLight(config['address'])

            device = AwoxMeshLightDevice(self)
            self.handle_device_added(device)
            if self.DEBUG:
                print("awox_mesh_light_device created")
            self.devices[device.id].connected = True
            self.devices[device.id].connected_notify(True)

        except Exception as ex:
            print("error: Could not create awox_mesh_light_device: " + str(ex))

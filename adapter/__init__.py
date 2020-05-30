# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>

"""AwoxMeshLight adapter for Mozilla WebThings Gateway."""

import os

from awoxmeshlight import AwoxMeshLight
from gateway_addon import Adapter
from .device import AwoxMeshLightDevice


MAC = os.getenv('MAC') or "A4:C1:38:FF:FF:FF"


class AwoxMeshLightAdapter(Adapter):
    """Adapter for Awox Mesh Light"""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """

        self.pairing = False
        self.addon_name = 'awox-mesh-light'
        self.DEBUG = True
        self.name = self.__class__.__name__
        self.URL = 'https://github.com/rzr/awox-mesh-light-webthing'
        Adapter.__init__(self,
                         self.addon_name, self.addon_name, verbose=verbose)

        try:
            self.controller = AwoxMeshLight(MAC)

            device = AwoxMeshLightDevice(self)
            self.handle_device_added(device)
            if self.DEBUG:
                print("awox_mesh_light_device created")
            self.devices[device.id].connected = True
            self.devices[device.id].connected_notify(True)

        except Exception as ex:
            print("error: Could not create awox_mesh_light_device: " + str(ex))

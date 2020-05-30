# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>
"""AwoxMeshLight adapter for Mozilla WebThings Gateway."""

from gateway_addon import Device, Property

_DEBUG = False

class AwoxMeshLightDevice(Device):
    """AwoxMeshLight device type."""

    def __init__(self, adapter):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        """
        Device.__init__(self, adapter, 'awox-mesh-light')
        self.id = self._id = 'awox-mesh-light'
        self.adapter = adapter

        self.name = 'AwoxMeshLight'
        self.description = 'Expose AwoxMeshLight actuators'
        self.links = [
            {
                'rel': 'alternate',
                'mediaType': 'text/html',
                'href': adapter.URL
            }
        ]
        self._type = []

        try:
            self.pairing = True

        except Exception as ex:
            print("error: Adding properties: " + str(ex))

class AwoxMeshLightProperty(Property):
    """Handle changes"""

    def __init__(self, device, name, description, value):
        Property.__init__(self, device, name, description)
        self.device = device
        self.title = name
        self.name = name
        self.description = description
        self.value = value
        self.set_cached_value(value)

    def set_value(self, value):
        """ Handle properties changes """
        if _DEBUG:
            print("info: awox_light_mesh." + self.name
                  + " from " + str(self.value) + " to " + str(value))
        if value == self.value:
            return

        self.set_cached_value(value)
        self.device.notify_property_changed(self)

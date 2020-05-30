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
        self.controller = adapter.controller
        self.controller.connect()
        _DEBUG and print(self.controller.getModelNumber())

        self.name = 'AwoxMeshLight'
        self.description = 'Expose AwoxMeshLight actuators'
        self.links = [
            {
                'rel': 'alternate',
                'mediaType': 'text/html',
                'href': adapter.URL
            }
        ]
        self._type = ['OnOffSwitch', 'MultiLevelSwitch', 'Light', 'ColorControl']

        try:
            self.properties['on'] = AwoxMeshLightProperty(
                self,
                "on",
                {
                    '@type': 'OnOffProperty',
                    'label': "Switch",
                    'type': 'boolean',
                    'description': 'Whether the lamp is turned on',
                },
                False)
            self.controller.off()

            self.properties['brightness'] = AwoxMeshLightProperty(
                self,
                "brightness",
                {
                    '@type': 'BrightnessProperty',
                    'label': 'Brightness',
                    'type': 'number',
                    'description': 'The level of light from 0-100',
                    'minimum': 0,
                    'maximum': 100,
                    'unit': 'percent'
                },
                100)
            self.controller.setColorBrightness(100)

            self.properties['color'] = AwoxMeshLightProperty(
                self,
                "color",
                {
                    '@type': 'ColorProperty',
                    'label': "Color",
                    'type': 'string',
                    'readOnly': False
                },
                '#ffffff')
            self.controller.setColor(0xFF, 0xFF, 0xFF)

            self.pairing = True

        except Exception as ex:
            print("error: Adding properties: " + str(ex))

    @staticmethod
    def hex_to_rgb(text):
        """ Convert #RRGGBB to list of integer [0-255]"""
        color = {"red": int(text[1:3], 0x10),
                 "green": int(text[3:5], 0x10),
                 "blue": int(text[5:7], 0x10)}
        return color

class AwoxMeshLightProperty(Property):
    """Handle changes with controller """

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
        if self.name == 'on':
            if bool(value):
                self.device.controller.on()
            else:
                self.device.controller.off()
        elif self.name == 'brightness':
            self.device.controller.setColorBrightness(int(value))
        elif self.name == 'color':
            color = AwoxMeshLightDevice.hex_to_rgb(value)
            self.device.controller.setColor(**color)

        self.set_cached_value(value)
        self.device.notify_property_changed(self)

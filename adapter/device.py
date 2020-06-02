# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>
"""AwoxMeshLight adapter for Mozilla WebThings Gateway."""

import os
import random

from gateway_addon import Action, Device, Property

_DEBUG = bool(os.getenv('DEBUG')) or False

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
        if _DEBUG:
            print("info: connecting: address=%s" % self.controller.mac)
        self.controller.connect()
        if _DEBUG:
            print("info: connected: model=%s" % self.controller.getModelNumber())

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
            self.properties['preset'] = AwoxMeshLightProperty(
                self,
                "preset",
                {
                    '@type': 'NumberProperty',
                    'label': "Preset",
                    'type': 'integer',
                    'enum': [0, # Red...
                             1, # Magenta...
                             2, # Yellow...
                             3, # Green...
                             4, # Blue...
                             5, # Blue (solid)
                             6  # Purple (solid)
                    ]
                },
                6)
            self.controller.setPreset(6);

            self.properties['on'] = AwoxMeshLightProperty(
                self,
                "on",
                {
                    '@type': 'OnOffProperty',
                    'label': "Switch",
                    'type': 'boolean',
                    'description': 'Whether the lamp is turned on',
                },
                True)
            self.controller.on()

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

            self.add_action(
                'cold',
                {
                    'title': 'Cold White'
                }
            )
            self.add_action(
                'warm',
                {
                    'title': 'Warm White'
                }
            )

            self.add_action(
                'random',
                {
                    'title': 'Random Color',
                }
            )
            self.pairing = True

        except Exception as ex:
            print("error: Adding properties: " + str(ex))

    def perform_action(self, action):
        if _DEBUG:
            print(action.__dict__)
        try:
            if action.name == 'random':
                color = "#%06x" % random.randint(0, 0xFFFFFF)
                self.set_property('color', color)
            elif action.name == 'cold':
                self.set_property('color', "#ffffff")
                self.set_property('brightness', 100)
                self.set_property('on', True)
                self.controller.setWhite(0x00, 0x7F)
            elif action.name == 'warm':
                self.set_property('color', "#ffffff")
                self.set_property('brightness', 100)
                self.set_property('on', True)
                self.controller.setWhite(0x73, 0x63)
        except Exception:
            if _DEBUG:
                print("error: Failed to set_property")

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
        try:
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
            elif self.name == 'preset':
                self.device.controller.setPreset(value)

            self.set_cached_value(value)
            self.device.notify_property_changed(self)
        except Exception:
            if _DEBUG:
                print("error: Failed to set_property")

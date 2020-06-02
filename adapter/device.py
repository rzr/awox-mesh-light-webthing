# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>
"""AwoxMeshLight adapter for Mozilla WebThings Gateway."""

import bluepy
import os
import random
import time

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
            self.add_action(
                'preset',
                {
                    'title': 'Fading preset',
                    'input': {
                        'type': 'object',
                        'required': [
                            'preset',
                        ],
                        'properties': {
                            'preset': {
                                'type': 'integer',                                
                                'default': 0,
                                'maximum': 6,
                                'minimum': 0
                            }
                        }
                    }
                }
            )
            self.pairing = True

        except Exception as ex:
            print("error: Adding properties: " + str(ex))

    def perform_action(self, action):
        if _DEBUG:
            print(action.__dict__)
        if action.name == 'random':
            color = "#%06x" % random.randint(0, 0xFFFFFF)
            self.set_property('color', color)
        elif action.name == 'cold':
            self.set_property('color', '#ffffff')
            self.set_property('brightness', 100)
            self.set_property('on', True)
            self.controller.setWhite(0x00, 0x7F)
        elif action.name == 'warm':
            self.set_property('color', '#ffffff')
            self.set_property('brightness', 100)
            self.set_property('on', True)
            self.controller.setWhite(0x73, 0x63)
        elif action.name == 'preset':
            self.set_property('color', '#ffffff')
            self.set_property('brightness', 100)
            self.set_property('on', True)
            self.controller.setPreset(action.input[action.name])

    @staticmethod
    def hex_to_rgb(text):
        """ Convert #RRGGBB to list of integer [0-255]"""
        color = {"red": int(text[1:3], 0x10),
                 "green": int(text[3:5], 0x10),
                 "blue": int(text[5:7], 0x10)}
        return color

    def control(self, name, value):
        try:
            if name == 'on':
                if (value):
                    self.controller.on()
                else:
                    self.controller.off()
            elif name == 'brightness':
                brightness = int(0x0A + ((0x64 - 0x0A) *  value / 100.))
                if _DEBUG:
                    print("brightness: 0x%02x" % brightness)
                    self.controller.setColorBrightness(brightness)
            elif name == 'color':
                color = AwoxMeshLightDevice.hex_to_rgb(value)
                self.controller.setColor(**color)
        except:
            if _DEBUG:
                print("error: Exception in control: ")
            self.reset()

    def reset(self):
        if _DEBUG:
            print("info: reset")
        try:
            self.controller.disconnect()
        finally:
            time.sleep(2)            
        try:
            self.controller.connect()
        finally:
            print("info: connected: model=%s" % self.controller.getModelNumber())



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
                self.device.control('color',
                                    self.device.properties['color'].value)
                self.device.control('brightness',
                                    self.device.properties['brightness'].value)
            self.device.control(self.name, value)
        elif self.name == 'brightness':
            if self.device.properties['on'].value:
                self.device.control('color',
                                    self.device.properties['color'].value)
                self.device.control(self.name, value)
        elif self.name == 'color':
            if self.device.properties['on'].value:
                self.device.control(self.name, value)

        self.set_cached_value(value)
        self.device.notify_property_changed(self)

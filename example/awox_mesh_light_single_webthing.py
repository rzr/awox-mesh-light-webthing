#!/usr/bin/env python3
# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>

"""Awox lamp example"""

import logging
import os

import awoxmeshlight

from webthing import (Property, SingleThing, Thing, Value,
                      WebThingServer)

PORT = os.getenv('PORT') or 8888
MAC = os.getenv('MAC') or "A4:C1:38:FF:FF:FF"

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

logger = logging.getLogger("awoxmeshlight")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

controller = awoxmeshlight.AwoxMeshLight(MAC)

def set_color(hexcode):

    red = hexcode[1:3]
    red = "0x%s" % str(red)
    red = int(red, 0x10)

    green = hexcode[3:5]
    green = "0x%s" % str(green)
    green = int(green, 0x10)

    blue = hexcode[5:7]
    blue = "0x%s" % str(blue)
    blue = int(blue, 0x10)

    try:
        controller.setColor(red, green, blue)
    except:
        print('error:')


def make_thing():
    thing = Thing('urn:dev:ops:my-awox-light-1234',
                  'Awox Light',
                  ['OnOffSwitch', 'Light'],
                  'A web connected lamp')

    thing.add_property(
        Property(thing,
                 'on',
                 Value(True, lambda v: controller.on() if v else controller.off()),
                 metadata={
                     '@type': 'OnOffProperty',
                     'label': 'On/Off',
                     'type': 'boolean',
                     'description': 'Whether the lamp is turned on',
                 }))

    thing.add_property(
        Property(thing,
                 'brightness',
                 Value(50, lambda v: controller.setColorBrightness(int(v))),
                 metadata={
                     '@type': 'BrightnessProperty',
                     'label': 'Brightness',
                     'type': 'number',
                     'description': 'The level of light from 0-100',
                     'minimum': 0,
                     'maximum': 100,
                     'unit': 'percent',
                 }))

    thing.add_property(
        Property(thing,
                 'color',
                 Value('#ffffff', lambda v: set_color(v)),
                 metadata={
                     '@type': 'ColorProperty',
                     'label': 'Color',
                     'type': 'string',
                     'description': 'Color of light',
                 }))


    return thing


def run_server():
    logging.info("controller: connect: %s" % MAC)
    controller.connect()
    logging.info("controller: model: %s" % controller.getModelNumber())
    thing = make_thing()
    server = WebThingServer(SingleThing(thing), port=PORT)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()

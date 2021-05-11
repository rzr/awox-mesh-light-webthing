#!/usr/bin/env python3
# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>

""" Gateway stub """

import os
import asyncio
import websockets

HOST = os.getenv('HOST') or 'localhost'
PORT = os.getenv('PORT') or 9500
VERBOSE = True

async def echo(websocket, path):
    """ handle incoming requests """
    async for message in websocket:
        if VERBOSE:
            print(path)
            print(message)
        await websocket.send(message)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, str(HOST), int(PORT)))
asyncio.get_event_loop().run_forever()

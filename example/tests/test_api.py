#!/usr/bin/env python3
# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr/>

""" API Tests """

import os
import requests

PORT = os.getenv('PORT') or '8888'
URL = os.getenv('URL') or ('http://localhost:' + PORT)

def check_property(name='on'):
    """ Generic property test """
    response = requests.get(URL + '/properties/' + name)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body[name] is not None


def test_get_check():
    """ default root endpoint test """
    response = requests.get(URL)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_get_check_properties():
    """ properties endpoint """
    response = requests.get(URL + '/properties')
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = response.json()
    assert response_body["on"] is not None
    assert response_body["brightness"] is not None
    assert response_body["color"] is not None

def test_get_check_property_on():
    check_property('on')

def test_get_check_property_brightness():
    check_property('brightness')

def test_get_check_property_color():
    check_property('color')

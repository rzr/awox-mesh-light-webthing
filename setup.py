# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT
# Copyright: Phil Coval <https://purl.org/rzr>

"""A setuptools based setup module."""

from codecs import open
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

requirements = [
]
URL = 'https://github.com/rzr/awox-mesh-light-webthing/'

setup(
    name='awox-mesh-light-webthing',
    version='0.0.5',
    description='Awox Mesh Light WebThing',
    long_description=long_description,
    url=URL,
    author='Philippe Coval',
    author_email='rzr@users.sf.net',
    keywords='Awox mesh light bluetooth mozilla iot web thing webthing',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT',
    project_urls={
        'Source': URL,
        'Tracker': URL + '/issues',
    },
    python_requires='>=3.7se, <4',
)

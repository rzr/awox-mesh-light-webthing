#!/bin/make -f
# -*- makefile -*-
# SPDX-License-Identifier: MIT
# Copyright: Philippe Coval <https://purl.org/rzr/>

default: help all

project?=awox-mesh-light-adapter
port?=8080
mac?=A4:C1:38:FF:FF:FF
webthing_port?=8888
webthing_url?=http://localhost:${webthing_port}

help:
	@echo "## Usage:"
	@echo "# make start # To start Webthings"
	@echo "# make aframe/start # To start browser"
	@echo "# make rule/version/X.Y.Z # To update manifest"

start: example/awox_mesh_light_single_webthing.py
	MAC=${mac} $<

demo:
	curl \
        "${webthing_url}/properties"
	curl \
	-X PUT --data '{"color": "#FFFFFF"}' \
        -H 'Content-Type: "application/json" ' \
        "${webthing_url}/properties/color"
	curl \
	-X PUT --data '{"brightness": 100}' \
        -H 'Content-Type: "application/json" ' \
        "${webthing_url}/properties/brightness"
	curl \
        "${webthing_url}/properties"
	curl \
	-X PUT --data '{"on": false}' \
        -H 'Content-Type: "application/json" ' \
        "${webthing_url}/properties/on"


aframe/start: extra/aframe
	@echo "# http://localhost:${port}/$<"
	python -m SimpleHTTPServer ${port}

rule/version/%: manifest.json package.json setup.py
	-git describe --tags
	sed -e "s|\(\"version\":\) .*|\1 \"${@F}\"|g" -i $<
	sed -e "s|\(\"version\":\) .*|\1 \"${@F}\",|g" -i package.json
	sed -e "s|\(.*version='\).*\('.*\)|\1${@F}\2|g" -i setup.py
	-git commit -sm "Release ${@F}" $^
	-git tag -sam "${project}-${@F}" "v${@F}" \
|| git tag -am "${project}-${@F}" "v${@F}"

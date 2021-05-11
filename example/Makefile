#!/bin/make -f
# -*- makefile -*-
# SPDX-License-Identifier: MIT
# Copyright: Philippe Coval <https://purl.org/rzr/>

default: help prep run

NAME?=unpaired
PASSWORD?=1234
MAC?=A4:C1:38:FF:FF:FF
pytest?=$(shell which pytest-3 || which pytest || echo pytest)

help:
	@echo "## Usage:"
	@echo "# make prep run"
	@echo "#  MAC=${MAC} NAME=${NAME} PASSWORD=${PASSWORD} make run"

prep: requirements.txt
	pip3 install -r${<F}

run: awox_mesh_light_single_webthing.py
	${<D}/${<F}

client: ../Makefile
	make -C ${<D} demo

test: tests
	${pytest} $<


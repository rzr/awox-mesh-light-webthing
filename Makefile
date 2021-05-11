#!/bin/make -f
# -*- makefile -*-
# SPDX-License-Identifier: MIT
# Copyright: Philippe Coval <https://purl.org/rzr/>

default: help all

project?=awox-mesh-light-adapter
project_url ?= https://github.com/rzr/awox-mesh-light-webthing
port?=8080
mac?=A4:C1:38:FF:FF:FF
webthing_port?=8888
webthing_url?=http://localhost:${webthing_port}
builder_url ?= https://github.com/WebThingsIO/addon-builder
builder_dir ?= tmp/addon-builder
module_dir ?= ${builder_dir}/${project}

gateway_addon_version?=v1.0.0
gateway_addon_url?=https://github.com/WebThingsIO/gateway-addon-python

addons_url ?= https://github.com/WebThingsIO/addon-list
addons_dir ?= tmp/addon-list
addons_json ?= ${addons_dir}/addons/${project}.json
addons_review_org ?= ${USER}
addons_review_branch ?= sandbox/${USER}/review/master
addons_review_url ?= ssh://github.com/${addons_review_org}/addon-list
addons_review_http_url ?= ${addons_url}/compare/master...${addons_review_org}:${addons_review_branch}?expand=1

python?=$(shell which python3 || which python || echo python)
pylint?=$(shell which pylint3 || which pylint || echo pylint)
pip?=$(shell which pip3 || which pip || echo pip)


help:
	@echo "## Usage:"
	@echo "# make start # To start Webthings"
	@echo "# make aframe/start # To start browser"
	@echo "# make rule/version/X.Y.Z # To update manifest"
	@echo "# make rule/release/X.Y.Z # To update addon-list"

start: example/awox_mesh_light_single_webthing.py
	MAC=${mac} $<

gateway_addon:
	git clone --branch ${gateway_addon_version} --depth 1 \
	  ${gateway_addon_url} $@
	cd $@ && ${pip} install -rrequirements.txt
	cd $@ && ${python} ./setup.py build

run: main.py gateway_addon
	PYTHONPATH=gateway_addon/gateway_addon/.. ${<D}/${<F}

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

rule/version/%: manifest.json setup.py
	-git describe --tags
	jq < "$<" | jq '.version |= "${@F}"' > "$<.tmp"
	jq < "$<.tmp" > "$<"
	rm -f "$<.tmp"
	sed -e "s|\(.*version='\).*\('.*\)|\1${@F}\2|g" -i setup.py
	-git commit -sm "Release ${@F}" $^
	-git tag -sam "${project}-${@F}" "v${@F}" \
|| git tag -am "${project}-${@F}" "v${@F}"

rule/builder: ${module_dir}
	cd ${<D} \
 && git commit -sam "${project}: Add module" \
 || git commit -am "${project}: Add module"

${module_dir}: ${builder_dir}
	cd $< && git submodule add ${project_url} ${project}
	cd "$@" && git describe --tags

${builder_dir}:
	mkdir -p ${@D}
	git clone ${builder_url} ${builder_dir}

rule/addons/push: ${addons_json}
	jq < "$<" > /dev/null
	cd ${<D} \
&& git --no-pager diff \
&& git commit -am "${project}: ${message}"
	@echo "# About to push to ${addons_review_url}"
	@echo "# Stop now with ctrl+c"
	sleep 5
	cd ${<D} \
&& git push ${addons_review_url} -f  HEAD:${addons_review_branch}
	@echo "# Request merge at"
	@echo "# ${addons_review_http_url}"

rule/release/%: ${addons_json} rule/version/%
	sed -e "s|\(.*\"version\": \)\"\(.*\)\"\(.*\)|\1\"${@F}\"\3|g" -i $<
	sed -e "s|\(.*/${project}-\)\([0-9.]*\)\(-.*\)|\1${@F}\3|g" -i $<
	${MAKE} rule/checksum/update
	-git diff
	${<D}/../tools/check-list.py ${project}
	${MAKE} rule/addons/push message="Update to ${@F}"

${addons_json}:
	mkdir -p "${addons_dir}"
	git clone ${addons_url} "${addons_dir}"
	jq < "$@"

tmp/urls.lst: ${addons_json}
	jq '.packages[].url' < "$<" | xargs -n1 echo > $@

tmp/checksums.lst: tmp/urls.lst Makefile
	cat $< | while read url ; do \
  curl -L -s -I "$${url}" | grep -r 'HTTP/1.1 {200,302}' > /dev/null \
  && curl -L -s "$${url}" | sha256sum - ; \
done \
| cut -d' ' -f1 | tee $@.tmp
	mv $@.tmp $@

rule/checksum/update: ${addons_json} tmp/checksums.lst
	cp -av "$<" "$<.tmp"
	i=0; \
  cat tmp/checksums.lst | while read sum ; do \
  jq '.packages['$${i}'].checksum |= "'$${sum}'"' < $<.tmp  > $<.out.tmp ; \
  mv "$<.out.tmp" "$<.tmp" ; \
  i=$$(expr 1 + $${i}) ; \
done
	jq < "$<.tmp" > /dev/null
	mv "$<.tmp" "$<"

rule/wait:
	@printf "# Scanning: "
	@while true ; do \
  ${MAKE} rule/urls | grep 'HTTP/1.1 200' && exit 0 \
  || printf "."; \
  sleep 1; \
done

rule/checksum/push: rule/wait rule/checksum/update
	${MAKE} rule/addons/push message="Update checksums from URLs"


lint:
	${pylint} --version
	${pylint} *.py */*.py

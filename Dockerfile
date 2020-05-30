#!/bin/echo docker build . -f
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright: Philippe Coval <https://purl.org/rzr/>

FROM python:3.7-buster
LABEL maintainer="Philippe Coval (rzr@users.sf.net)"

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL en_US.UTF-8
ENV LANG ${LC_ALL}

ENV project awox-mesh-light-adapter
ENV workdir /root/.mozilla-iot/addons/${project}
ADD . ${workdir}

WORKDIR ${workdir}

RUN echo "# log: ${project}: Setup system" \
  && set -x \
  && apt-get clean \
  && apt-get update \
  && sync

RUN echo "# log: ${project}: Building package" \
  && set -x \
  && ./package.sh \
  && sync

WORKDIR ${workdir}
RUN echo "# log: ${project}: Distribute package" \
  && set -x \
  && install -d /usr/local/opt/${project}/dist \
  && install ${project}-*.tgz /usr/local/opt/${project}/dist \
  && tar tvfz /usr/local/opt/${project}/dist/${project}-*.tgz \
  && sha256sum /usr/local/opt/${project}/dist/* \
  && sync

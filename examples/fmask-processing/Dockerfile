# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM mambaorg/micromamba:jammy

USER root

#
# Install base dependencies
#
RUN apt update -y \
    && apt install \
        git \
        make \
        -y \
    && rm -rf /var/lib/apt/lists/*

USER mambauser

#
# Base python packages
#
COPY environment.yml environment.yml

RUN micromamba create -n fmask -f environment.yml --yes \
    && micromamba run -n fmask pip3 install git+https://github.com/storm-platform/storm-workbench.git

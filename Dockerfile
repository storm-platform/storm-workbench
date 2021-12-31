# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM jupyter/minimal-notebook:lab-3.2.5

#
# Base dependencies
#
RUN pip install --upgrade \
    setuptools \
    wheel \
    pip

#
# Storm Workbench
#
COPY . /opt/app/workbench
# RUN pip install /opt/app/workbench[cli]

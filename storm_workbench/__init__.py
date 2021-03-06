# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Workbench manager for Storm platform."""

from .version import __version__

from .workbench import Workbench

__all__ = (
    "__version__",
    "Workbench",
)

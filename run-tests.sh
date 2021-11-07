#!/usr/bin/env bash
#
# This file is part of Workbench manager for Storm platform.
# Copyright (C) 2021 INPE.
#
# Workbench manager for Storm platform is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

pydocstyle storm_workbench examples tests setup.py && \
isort storm_workbench examples tests setup.py --check-only --diff && \
check-manifest --ignore ".travis.yml,.drone.yml,.readthedocs.yml" && \
sphinx-build -qnW --color -b doctest docs/sphinx/ docs/sphinx/_build/doctest && \
pytest

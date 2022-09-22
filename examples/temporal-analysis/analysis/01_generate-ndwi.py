# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

from compendium import ndwi2

#
# General definitions
#

# CBERS-4a/AWFI - Band 14 brick (2018-08-31 to 2019-08-31)
brick_green_input = Path('data/input_data/bricks/brick-cbers4-awfi-band14.tif')

# CBERS-4a/AWFI - Band 16 brick (2018-08-31 to 2019-08-31)
brick_nir_input = Path('data/input_data/bricks/brick-cbers4-awfi-band16.tif')

# Output
brick_output = Path('data/derived_data/brick-cbers4-awfi-ndwi2.tif')

#
# 1. Generating NDWI
#
ndwi2(brick_green_input, brick_nir_input, brick_output)

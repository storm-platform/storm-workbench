# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

import pandas as pd
import geopandas as gpd

import rasterio as rio

#
# General definitions
#

# Input brick
brick_input = Path("data/derived_data/brick-cbers4-awfi-ndwi2.tif")

# Water points available in the application ROI.
samples_input = Path("data/input_data/samples/samples-water.shp")

# Output data
table_output = Path("data/derived_data/sample-water-timeseries.csv")

#
# 1. Loading brick
#
brick_ds = rio.open(brick_input)

#
# 2. Loading samples
#
samples = gpd.read_file(samples_input)

#
# 3. Converting samples CRS to be the same in the image
#
samples = samples.to_crs(brick_ds.crs)

#
# 4. Extracting data from brick
#
samples_extracted = brick_ds.sample([(p.x, p.y) for p in samples.geometry])
samples_extracted = list(samples_extracted)

#
# 5. Saving the result
#
pd.DataFrame(samples_extracted).T.to_csv(table_output)

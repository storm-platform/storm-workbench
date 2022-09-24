# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Gallery.
#
# storm-gallery is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import urllib

import os
from pathlib import Path

from toolbox import generate_brick, crop_brick_by_polygon

import rasterio as rio
import geopandas as gpd

from pystac_client import Client as StacClient

#
# General definitions
#

# API definitions
access_token = ""
stac_api_address = "https://brazildatacube.dpi.inpe.br/stac"

# Data definitions
start_date = "2018-08-31"
end_date = "2019-08-31"

collection = "CB4_64_16D_STK-1"

bbox = [-47.8455, -20.9820, -45.4504, -18.9271]

spatial_extent_shapefile = gpd.read_file(
    "data/raw_data/data-package.gpkg", layer="extent"
)

# Results variables
bricks = {"green": [], "nir": []}

# Output definitions
output_dir = Path("data/derived_data")
output_dir.mkdir(parents=True, exist_ok=True)

output_dir_green_band = output_dir / "green"
output_dir_green_band.mkdir(parents=True, exist_ok=True)

output_dir_nir_band = output_dir / "nir"
output_dir_nir_band.mkdir(parents=True, exist_ok=True)

#
# 1. Searching for images on STAC
#

# 1.1. Creating stac client
stac_client = StacClient.open(
    stac_api_address, parameters=dict(access_token=access_token)
)

# 1.2. Searching results
search_result = stac_client.search(
    bbox=bbox,
    collections=collection,
    datetime=f"{start_date}/{end_date}",
)

items = search_result.items()

#
# 2. Download satellite data
#
for item in items:
    print(f"Processing: {item.id}")

    nir_asset = item.assets["BAND16"]  # NIR
    green_asset = item.assets["BAND14"]  # Green

    nir_asset_file = str(
        output_dir_nir_band / os.path.basename(nir_asset.href).split("?")[0]
    )
    green_asset_file = str(
        output_dir_green_band / os.path.basename(green_asset.href).split("?")[0]
    )

    urllib.request.urlretrieve(nir_asset.href, nir_asset_file)
    urllib.request.urlretrieve(green_asset.href, green_asset_file)

    bricks["nir"].append(nir_asset_file)
    bricks["green"].append(green_asset_file)

#
# 3. Generating brick files
#

# 3.1. Green Band brick
green_brick_file = output_dir_green_band / "brick.tif"

generate_brick(bricks["green"], green_brick_file)

# 3.2. NIR Band brick
nir_brick_file = output_dir_nir_band / "brick.tif"

generate_brick(bricks["nir"], nir_brick_file)

#
# 4. Cropping the generated bricks
#

# configuring the roi polygon
reference_crs = rio.open(green_brick_file).crs
spatial_extent_shapefile = spatial_extent_shapefile.to_crs(reference_crs)

polygon_geometry = [
    gpd.GeoSeries(spatial_extent_shapefile.unary_union).__geo_interface__["features"][
        0
    ]["geometry"]
]

# 4.1. Green Band brick
green_brick_cropped = output_dir_green_band / "brick_roi.tif"

crop_brick_by_polygon(green_brick_file, green_brick_cropped, polygon_geometry)

# 4.2. NIR Band brick
nir_brick_cropped = output_dir_nir_band / "brick_roi.tif"

crop_brick_by_polygon(nir_brick_file, nir_brick_cropped, polygon_geometry)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Gallery.
#
# storm-gallery is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import rasterio as rio
import rasterio.mask as rio_mask

from natsort import natsorted


def generate_brick(brick_files, brick_output_file):
    """Generate brick from list of raster files with same
    spatial and tempora extension."""
    with rio.Env():
        # sorting files
        brick_files = natsorted(brick_files)

        first_image = rio.open(brick_files[0])

        profile = first_image.profile
        profile.update(dict(count=len(brick_files)))

        with rio.open(brick_output_file, "w", **profile) as dst:
            for idx, brick_file in enumerate(brick_files):

                _data = rio.open(brick_file)
                dst.write(_data.read()[0], idx + 1)


def crop_brick_by_polygon(brick_file, brick_output, polygon_geometry):
    """Crop brick by polygon geometry (as list of list)."""
    with rio.open(brick_file) as _data:
        out_image, out_transform = rio_mask.mask(_data, polygon_geometry, crop=True)
        out_meta = _data.meta

        # defining output information
        out_meta.update(
            {
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
            }
        )

        with rio.open(brick_output, "w", **out_meta) as dest:
            dest.write(out_image.astype(out_meta["dtype"]))

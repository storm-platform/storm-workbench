# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import Tuple
from pathlib import Path

import rasterio as rio

from joblib import Parallel, delayed


def _ndwi2(
    brick_green: str, brick_nir: str, layer_idx: str, window: rio.windows.Window
) -> Tuple:
    """Calculate the Normalized Difference Water Index (NDWI2)."""
    nir = rio.open(brick_nir, count=layer_idx).read(window=window)
    green = rio.open(brick_green, count=layer_idx).read(window=window)

    return (green - nir) / (green + nir), window


def ndwi2(
    brick_green_input: Path, brick_nir_input: Path, brick_output: Path, n_jobs: int = 3
) -> Path:
    """Calculate the Normalized Difference Water Index (NDWI2).

    Args:
        brick_green_input (str): The path to the green brick file.

        brick_nir_input (str): The path to the nir brick file.

        brick_output (rio.windows.Window): The path to the result brick file.

        n_jobs (int): Number of processors used to generated the result.

    Returns:
        str: Path where NDWI Brick was saved.

    See:
        - McFeeters, S. K., 1996. The use of the Normalized Difference Water Index (NDWI) in
          the delineation of open water features. International Journal ofRemote Sensing, 17(7), 1425-1432.

        - rasterio.windows module: https://rasterio.readthedocs.io/en/latest/api/rasterio.windows.html
    Note:
        The `rio.windows.Window` is an object that allows you to determine the region of the raster to be processed. The `window` parameter
        accepts this object and allows only a portion of the scene to be processed. This can be used as a base strategy for
        parallelizing the NDWI2 calculation operation.
    """
    brick_output = Path(brick_output)

    brick_green_input = Path(brick_green_input)
    brick_nir_input = Path(brick_nir_input)

    if not all(
        [b.exists() or b.is_dir()] for b in [brick_green_input, brick_nir_input]
    ):
        raise ValueError(
            "Invalid input. This brick paths must be a valid `brick raster` file."
        )

    # loading the brick and calculate the ndwi2
    brick_ds_1 = rio.open(brick_green_input)
    brick_ds_2 = rio.open(brick_nir_input)

    reference = brick_ds_1

    assert brick_ds_1.count == brick_ds_2.count
    assert brick_ds_1.shape == brick_ds_2.shape

    profile = brick_ds_1.profile.copy()
    profile.update(dict(dtype="float32", driver="GTiff"))

    with rio.open(brick_output, "w", **profile) as dst:
        for layer_idx in range(1, reference.count + 1):
            # split image into mini-rasters
            windows = list(map(lambda x: x[1], list(reference.block_windows())))

            # processing in a parallel way
            water_mini_rasters = Parallel(n_jobs=n_jobs)(
                delayed(_ndwi2)(
                    brick_green_input,
                    brick_nir_input,
                    layer_idx,
                    window,
                )
                for window in windows
            )

            # save the water mask raster result
            for mini_raster_data, window in water_mini_rasters:
                dst.write(mini_raster_data, window=window)

    return brick_output

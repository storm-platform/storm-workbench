#
# This file is part of Workbench manager for Storm platform.
# Copyright (C) 2021 INPE.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Configuration options for storm-workbench."""


class WorkbenchDefinitions:
    WB_STORE_DIR = ".storm"

    WB_SECRETS_FILE = ".secrets.toml"
    WB_DEFINITION_FILE = "workbench.toml"

    WB_FILES_CHECKSUM_ALGORITHM = "sha256"

    WB_DEFAULT_EXECUTOR = "paradag.parallel"
    WB_DEFAULT_EXECUTOR_OPTIONS = {"n_processors": 1}

    # ToDo: List executors using entrypoint
    WB_AVAILABLE_EXECUTORS = {
        "ray.distributed": "storm_core.engine.executor.backends.ray.backend.RayBackend",
        "paradag.parallel": "storm_core.engine.executor.backends.paradag.backend.ParaDagBackend"
    }

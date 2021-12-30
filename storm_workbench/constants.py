# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


class WorkbenchDefinitions:
    """Base workbench configurations."""

    WB_DEFINITION_FILE = "workbench.toml"

    WB_DEFAULT_EXECUTOR = "paradag.parallel"

    WB_AVAILABLE_EXECUTORS = {
        "ray.distributed": "storm_core.execution.executor.backend.ray.backend:RayBackend",
        "paradag.parallel": "storm_core.execution.executor.backend.paradag.backend:ParadagBackend",
    }


class GraphStyleConfig:
    """Graph Style configuration."""

    GRAPH_DEFAULT_VERTICES_COLOR = {"updated": "green", "outdated": "yellow"}

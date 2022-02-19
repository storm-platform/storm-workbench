# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

#
# Storm Core definitions
#
CORE_EXECUTOR_ENTRYPOINT = "core.executors"

#
# Storm Core descriptor
#
import storm_core

# ToDo: This metadata should be provided by the Storm Core ?
CORE_DESCRIPTOR_NAME = "Storm Core"
CORE_DESCRIPTOR_URI = "https://github.com/storm-platform/storm-core"
CORE_DESCRIPTION_VERSION = storm_core.__version__

#
# Storm Workbench definitions.
#
WB_SECRETS_FILE = ".secrets.toml"

WB_DEFINITION_FILE = "workbench.toml"

WB_DEFAULT_EXECUTOR = "paradag.parallel"

#
# Graph default visualization definitions.
#
GRAPH_DEFAULT_VERTICES_COLOR = {"updated": "green", "outdated": "yellow"}

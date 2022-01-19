# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

try:
    import rich
except ImportError:
    raise ModuleNotFoundError(
        "To use the CLI command, please, install the rich library: "
        "`pip install rich` or `poetry add rich`"
    )

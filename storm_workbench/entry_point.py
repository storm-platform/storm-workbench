# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import pkg_resources


def load_entry_point(entry_point_group: str):
    """Load entry point group.

    Args:
        entry_point_group (str): Entry Point group to load.

    Returns:
        List[object]: List with the loaded objects from the
        entry point group.
    """
    entry_point_definitions = []
    for entry_point in pkg_resources.iter_entry_points(group=entry_point_group):
        entry_point_obj = entry_point.load()

        entry_point_definitions.append(entry_point_obj)
    return entry_point_definitions

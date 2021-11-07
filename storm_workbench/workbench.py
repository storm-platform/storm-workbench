#
# This file is part of Workbench manager for Storm platform.
# Copyright (C) 2021 INPE.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Workbench module."""

from pathlib import Path
from typing import Union

from copy import copy

from .constants import WorkbenchDefinitions
from .settings.api import WorkbenchSettings


class StormWorkbench:

    def __init__(self, workbench_base_directory: Union[Path, str]):
        self._workbench_base_directory = workbench_base_directory
        self._workbench_store = Path(workbench_base_directory) / WorkbenchDefinitions.WB_STORE_DIR

        self._workbench_settings = WorkbenchSettings(self._workbench_store)

    @classmethod
    def init(cls, workbench_base_directory: Union[Path, str]):
        workbench_base_directory = Path(workbench_base_directory)

        # checking the base directory
        if not workbench_base_directory.is_dir():
            raise NotADirectoryError(f"`{workbench_base_directory}` is not a directory!")

        workbench_store = workbench_base_directory / WorkbenchDefinitions.WB_STORE_DIR
        workbench_store = workbench_store.expanduser()

        if workbench_store.is_dir():
            raise FileExistsError(f"`{workbench_store}` already exists")

        # creating the configurations
        workbench_store.mkdir()
        WorkbenchSettings.init(workbench_store)

        return cls(workbench_base_directory)

    def export(self, output_path: Union[Path, str]):  # ToDo
        ...

    @property
    def settings(self):
        return copy(self._workbench_settings)

    @property
    def execution(self):  # ToDo
        ...  # execution [exec and management] api accessor

    @property
    def service(self):  # ToDo
        ...  # service api accessor


__all__ = (
    "StormWorkbench"
)

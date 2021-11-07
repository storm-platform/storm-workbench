#
# This file is part of Workbench manager for Storm platform.
# Copyright (C) 2021 INPE.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

import toml
from dynaconf import Dynaconf

from pathlib import Path
from typing import Union

from ..constants import WorkbenchDefinitions


def _check_is_directory(directory: Path):
    """Check if directory exists."""
    if not directory.is_dir():
        raise NotADirectoryError(f"Invalid directory `{directory}`")


class WorkbenchSettings:

    def __init__(self, workbench_store: Union[Path, str]):
        self._workbench_store = Path(workbench_store)

        _check_is_directory(self._workbench_store)

        # configuration properties
        self._secrets = self._workbench_store / WorkbenchDefinitions.WB_SECRETS_FILE
        self._workbech_definition = self._workbench_store / WorkbenchDefinitions.WB_DEFINITION_FILE

        # load the configuration file
        self._settings = Dynaconf(
            settings_files=[self._secrets, self._workbech_definition]
        )

    def __copy__(self):
        """Create a copy instance of the workbench settings."""
        return WorkbenchSettings(self._workbench_store)

    def __deepcopy__(self, memodict={}):
        """Create a deepcopy instance of the workbench settings."""
        return WorkbenchSettings(self._workbench_store)

    @classmethod
    def init(cls, workbench_store: Union[Path, str]):
        workbench_store = Path(workbench_store)

        _check_is_directory(workbench_store)

        # generating base secret file
        secrets_file_path = workbench_store / WorkbenchDefinitions.WB_SECRETS_FILE
        _secrets_base_config = {
            "variables": {},
            "vault": {}
        }

        with open(secrets_file_path, "w") as ofile:
            toml.dump(_secrets_base_config, ofile)

        # generating base workbench definition file
        workbench_definition_file = workbench_store / WorkbenchDefinitions.WB_DEFINITION_FILE

        _workbench_base_config = {
            "files": {
                "data_storage": {},
                "ignored_objects": {},
                "checksum_algorithm": WorkbenchDefinitions.WB_FILES_CHECKSUM_ALGORITHM
            },
            "executor": {
                "executor_cls": WorkbenchDefinitions.WB_DEFAULT_EXECUTOR,
                "executor_ops": WorkbenchDefinitions.WB_DEFAULT_EXECUTOR_OPTIONS
            }
        }

        with open(workbench_definition_file, "w") as ofile:
            toml.dump(_workbench_base_config, ofile)

        return cls(workbench_store)


__all__ = (
    "WorkbenchSettings"
)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path
from typing import Union

from dynaconf import Dynaconf
from dynaconf import loaders
from dynaconf.utils.boxing import DynaBox

from storm_workbench import constants


class WorkbenchDefinitionFile:
    """Workbench definition class."""

    def __init__(self, filepath: Union[str, Path] = None, config: Dynaconf = None):
        """Initializer

        Args:
            filepath (Union[str, Path]): Path to the Workbench definition file.

            config (Dynaconf): Dynaconf configuration object with the Workbench definitions.
        """
        self._config = config
        self._filepath = filepath

    @property
    def definitions(self):
        """Workbench configuration definition."""
        return self._config  # ToDo: Review this method name!

    @property
    def filepath(self):
        """Path to the Workbench definition file."""
        return self._filepath

    def save(self):
        """Save the Workbench definition file."""
        data = self.definitions.as_dict()
        loaders.write(str(self.filepath), DynaBox(data).to_dict())

    @classmethod
    def load(cls, cwd):
        """Load the workbench configuration files.

        This function loads the workbench definition file and the user's secrets file.

        Args:
            cwd (Path): Base directory to find the workbench definition files.

        Returns:
            Dynaconf: Configuration object.

        Raises:
            RuntimeError: When the workbench definition file is not found.
        """
        # loading the workbench definition file
        workbench_definition_file = find_workbench_definition_file(cwd)

        # secret and context file
        workbench_secrets = workbench_definition_file.parent / ".secrets.toml"

        # loading configurations
        workbench_configuration = Dynaconf(
            settings_files=[workbench_definition_file],
            secrets=workbench_secrets,
        )

        # saving the loaded files
        workbench_configuration.tool.storm.basepath = workbench_definition_file.parent

        workbench_configuration.tool.storm.secrets_file = workbench_secrets
        workbench_configuration.tool.storm.definition_file = workbench_definition_file

        return cls(workbench_definition_file, workbench_configuration)


def find_workbench_definition_file(cwd: Path = None) -> Path:
    """Find for a workbench definition file.

    This function finds a workbench definition file in the ``cwd`` directory
    and their parents.

    Args:
        cwd (Path): Base directory where the search will be start.

    Returns:
        Path: Path to the founded workbench definition file.

    Raises:
        RuntimeError: When the workbench definition file is not found.

    Note:
        This function was adapted from the ``python-poetry`` source code. Currently, we only support the Linux
        implementation.

    See:
        See the original implementation of this function in the ``python-poetry``
        repository: <https://github.com/python-poetry/poetry-core/blob/af08f1ce720da467c9bf3d43eed3d9ebaf4ad7fb/src/poetry/core/factory.py#L438>
    """
    cwd = Path(cwd or Path.cwd())
    candidates = [cwd]
    candidates.extend(cwd.parents)

    for path in candidates:
        workbench_file = path / constants.WB_DEFINITION_FILE

        if workbench_file.exists():
            return workbench_file

    else:
        # Maybe we need to change this to another place!
        raise RuntimeError("Workbench not found!")


def find_secrets_file(cwd: Path = None) -> Union[None, Path]:
    """Find for a workbench secrets file.

    This function finds a workbench secrets file in the ``cwd`` directory
    and their parents.

    Args:
        cwd (Path): Base directory where the search will be start.

    Returns:
        Union[None, Path]: Path to the founded workbench secrets file or None when the secrets file
                           is not available.

    Note:
        This function was adapted from the ``python-poetry`` source code. Currently, we only support the Linux
        implementation.

    See:
        See the original implementation of this function in the ``python-poetry``
        repository: <https://github.com/python-poetry/poetry-core/blob/af08f1ce720da467c9bf3d43eed3d9ebaf4ad7fb/src/poetry/core/factory.py#L438>
    """
    cwd = Path(cwd or Path.cwd())
    candidates = [cwd]
    candidates.extend(cwd.parents)

    for path in candidates:
        secrets_file = path / constants.WB_SECRETS_FILE

        if secrets_file.exists():
            return secrets_file

    return None

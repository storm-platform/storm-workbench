# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import inspect
from copy import deepcopy
from functools import wraps
from pathlib import Path

from storm_workbench.exceptions import ConfigurationError
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class WorkbenchConfigurationStore:
    """Single source of truth for the workbench definitions."""

    _configuration_object = None

    @classmethod
    def load_config(cls, cwd: Path):
        """Load the workbench configuration."""
        cls._configuration_object = WorkbenchDefinitionFile.load(cwd)

    @classmethod
    def get_config(cls):
        """Get the current workbench configuration."""
        if not cls._configuration_object:
            raise ConfigurationError(
                "Configuration is not defined yet. Please, define it "
                "using the `load_config` method."
            )
        return deepcopy(cls._configuration_object)  # read-only!


def pass_config(f):
    """Decorator to load and inject the configuration
    object in a function."""

    @wraps(f)
    def wrapper(self, *args, **kwargs):

        # checking if the configuration is already defined
        is_configuration_already_defined = (
            False
            if not args
            else any([isinstance(arg, WorkbenchDefinitionFile) for arg in args])
        )

        if not is_configuration_already_defined:

            # defining the cwd
            cwd = None
            if "cwd" in inspect.getfullargspec(f).args:
                cwd = args[0] if args and type(args[0]) == Path else None

            # loading the configuration
            WorkbenchConfigurationStore.load_config(cwd)

            kwargs.update(
                dict(
                    config=WorkbenchConfigurationStore.get_config(),
                )
            )

        # injecting!
        return f(self, *args, **kwargs)

    return wrapper

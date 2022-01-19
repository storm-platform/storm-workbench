# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


class InvalidCommand(ValueError):
    """Raised when the command cannot be loaded/validated."""


class ConfigurationError(RuntimeError):
    """Raised when the configuration cannot be loaded/validated."""


class ExecutionCompendiumNotFound(RuntimeError):
    """Raised when the Execution Compendium is not found in the database/service."""

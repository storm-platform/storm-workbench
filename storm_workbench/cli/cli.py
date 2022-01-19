# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from importlib import import_module

from . import BASE_CLI_MODULE, COMMAND_MODULES


@click.group()
@click.version_option()
def workbench_cli():
    """Storm Workbench CLI."""


# Registering the available commands.
for command_module in COMMAND_MODULES:
    command_module_path = f"{BASE_CLI_MODULE}.{command_module}"

    mod = import_module(command_module_path)
    mod.register_command(workbench_cli)

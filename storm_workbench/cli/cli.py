# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click

from storm_workbench.cli.commands.environment import env
from storm_workbench.cli.commands.index import index
from storm_workbench.cli.commands.operation import operation
from storm_workbench.cli.commands.workbench import init


@click.group()
@click.version_option()
def workbench_cli():
    """Storm Workbench CLI."""


workbench_cli.add_command(env)
workbench_cli.add_command(init)
workbench_cli.add_command(index)
workbench_cli.add_command(operation)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click

from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.tree import aesthetic_tree_base
from storm_workbench.workbench import Workbench


@click.group(name="env")
@click.pass_context
def env(ctx):
    """Workbench Environment management."""
    if ctx.obj is None:
        ctx.obj = dict()

    try:
        ctx.obj["workbench"] = Workbench()
    except:
        aesthetic_traceback(show_locals=True)
        exit()


@env.command(name="info")
@click.pass_obj
def env_info(obj):
    """Workbench Environment info."""
    workbench = obj["workbench"]

    # getting the current workbench storage.
    environment_path = workbench.stage.environment.path
    environment_size = workbench.stage.environment.size

    # creating the description tree.
    tree = aesthetic_tree_base(
        title="\n[bold]Environment description[/bold]",
        children=[
            f"[blue]ID[/blue]: {environment_path.name}",
            f"[blue]Path[/blue]: {environment_path} ([yellow]{environment_size}[/yellow])",
        ],
    )

    aesthetic_print(tree)


@env.command(name="clean")
@click.pass_obj
def env_clean(obj):
    """Remove all files from the Workbench environment."""
    remove = click.confirm(
        "This command will remove all Execution Compendia registered "
        "(files and metadata) from the current Workbench "
        "environment. Are you sure you want to continue ?",
        abort=True,
    )

    if remove:
        try:
            workbench = obj["workbench"]
            workbench.stage.environment.clean()

            aesthetic_print("Storage cleaned!", 0)
        except:
            aesthetic_traceback(show_locals=True)


def register_command(ctx):
    """Register the command in a context."""
    ctx.add_command(env)

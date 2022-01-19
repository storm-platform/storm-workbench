# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.tree import aesthetic_tree_base


@service.group(name="context")
def context():
    """Context management."""


@context.command(name="info")
@click.pass_obj
def context_info(obj):
    """Context info."""
    workbench = obj["workbench"]

    # getting the current context info
    context_project = workbench.stage.ws.context.project

    # creating the description tree.
    tree = aesthetic_tree_base(
        title="\n[bold]Current context description[/bold]",
        children=[f"[blue]Project[/blue]: {context_project}"],
    )

    aesthetic_print(tree)


@context.command(name="update")
@click.option(
    "--project-id",
    required=True,
    type=str,
    help="Project identifier.",
)
@click.pass_obj
def context_update(obj, project_id=None):
    """Update the current activated entities in the context."""
    workbench = obj["workbench"]

    try:
        workbench.stage.ws.context.activate_project(project_id)
        aesthetic_print("Context updated!", 0)

    except:
        aesthetic_traceback(show_locals=True)

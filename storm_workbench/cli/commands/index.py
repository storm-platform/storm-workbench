# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from storm_core.helper.plotting import (
    plot_styled_indexed_executions,
    plot_dot_indexed_executions,
)

from storm_workbench.cli.graphics.aesthetic import aesthetic_traceback, aesthetic_print
from storm_workbench.cli.graphics.graph import show_ascii_graph
from storm_workbench.cli.graphics.table import aesthetic_table_index_ls
from storm_workbench.workbench import Workbench


@click.group(name="index")
@click.pass_context
def index(ctx):
    """Execution Compendia Index management."""
    if ctx.obj is None:
        ctx.obj = dict()

    try:
        ctx.obj["workbench"] = Workbench()
    except:
        aesthetic_traceback(show_locals=True)
        exit()


@index.command(name="ls")
@click.option(
    "-f",
    "--filter",
    required=False,
    is_flag=False,
    default=False,
    type=str,
    help="Filter option to filter the execution compendia. The filter "
    "is expressed as a dictionary (e.g., property=value). You can"
    "use all available properties to create the filter.",
)
@click.pass_obj
def index_ls(obj, filter=None):
    """List the Execution Compendia."""

    # getting the workbench
    workbench = obj["workbench"]

    try:
        # getting the available execution compendia
        execution_compendia = workbench.stage.index.query(_params=filter)

        # creating the compendium table
        aesthetic_table_index_ls(execution_compendia)
    except:
        aesthetic_traceback(show_locals=True)


@index.command(name="rm")
@click.option(
    "-n",
    "--name",
    required=True,
    is_flag=False,
    type=str,
    help="Name of the Execution Compendium to remove.",
)
@click.option(
    "--remove-related-compendia/--no-remove-related-compendia",
    is_flag=True,
    default=True,
    help="Flag indicating if the Execution Compendia related to the "
    "compendium that will be removed should also be removed.",
)
@click.pass_obj
def index_rm(obj, name=None, remove_related_compendia=True):
    """Remove an Execution Compendium."""
    # getting the workbench
    workbench = obj["workbench"]

    try:
        aesthetic_print(
            "[bold cyan]Storm Workbench[/bold cyan]: Removing the selected Execution Compendium",
            0,
        )

        # removing the selected execution compendium
        workbench.stage.index.remove_record(
            name=name, remove_related_compendia=remove_related_compendia
        )

        # creating the compendium table
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Done!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@index.command(name="edit")
@click.option(
    "-n",
    "--name",
    required=True,
    is_flag=False,
    type=str,
    help="Name of the Execution Compendium to edit.",
)
@click.option(
    "-d",
    "--description",
    required=True,
    is_flag=False,
    help="Execution Compendium description",
)
@click.pass_obj
def index_edit(obj, name=None, description=None):
    """Edit an Execution Compendium."""
    # getting the workbench
    workbench = obj["workbench"]

    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Editing the selected Execution Compendium",
        0,
    )

    try:
        # getting the selected execution compendia
        execution_compendium = workbench.stage.index.query(name=name)

        if execution_compendium:
            execution_compendium = execution_compendium[0]
            execution_compendium.description = description

            workbench.stage.index.upsert_record(execution_compendium)

        # creating the compendium table
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Done!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@index.command(name="graph")
@click.option(
    "--to-dot",
    required=False,
    is_flag=True,
    default=False,
    help="Flag indicating that the execution Directed Acyclic Graph (DAG) "
    "should be saved in a ``dot`` file.",
)
@click.option(
    "--render-dot",
    required=False,
    is_flag=True,
    default=False,
    help="Flag indicating that the execution Directed Acyclic Graph (DAG) "
    "should be rendered in a ``png`` file based on a ``dot`` file (Require "
    "``--to-dot`` flag).",
)
@click.option(
    "--to-png",
    required=False,
    is_flag=True,
    default=False,
    help="Flag indicating that the execution Directed Acyclic Graph (DAG) "
    "should be rendered in a ``png`` file based on a ``igraph.plotting`` "
    "module.",
)
@click.option(
    "--filename",
    required=False,
    is_flag=False,
    default="graph",
    help="Filename used to save the graph files (``.dot``, ``.png``).",
)
@click.pass_obj
def index_graph(obj, to_dot, render_dot, to_png, filename):
    """Visualize the Execution Index as a Directed Acyclic Graph (DAG)."""
    workbench = obj["workbench"]
    graph_manager = workbench.backstage.execution.index.graph_manager

    try:
        if not graph_manager.is_empty:
            aesthetic_print("[bold]Execution Compendia index as DAG[bold]", 0)

            if to_dot or render_dot:
                filename = f"{filename}.dot"

                aesthetic_print(
                    f"Rendering the DAG in a [bold]dot[/bold] file ({filename}).", 0
                )
                plot_dot_indexed_executions(
                    graph_manager, filename=filename, render=render_dot
                )

            if to_png:
                filename = f"{filename}.png"

                aesthetic_print(
                    f"Rendering the DAG in a [bold]png[/bold] file ({filename}).", 0
                )
                plot_styled_indexed_executions(graph_manager, filename=filename)

            if not any([to_dot, to_png]):
                show_ascii_graph(graph_manager.graph)
        else:
            aesthetic_print("There is no indexed execution in this Workbench!", 0)
    except:
        aesthetic_traceback(show_locals=True)


def register_command(ctx):
    """Register the command in a context."""
    ctx.add_command(index)

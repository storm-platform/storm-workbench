# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click


from storm_workbench.workbench import Workbench

from storm_core.helper.plotting import (
    plot_styled_indexed_executions,
    plot_dot_indexed_executions,
)

from storm_workbench.cli.graphics.graph import show_ascii_graph
from storm_workbench.cli.graphics.aesthetic import aesthetic_print
from storm_workbench.cli.graphics.table import show_table_execution_index_status


@click.group(name="index")
@click.pass_context
def index(ctx):
    """Execution index management."""
    if ctx.obj is None:
        ctx.obj = dict()

    ctx.obj["workbench"] = Workbench()


@index.command(name="list")
@click.option(
    "--as-graph",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to indicate that the executions should be presented as a graph.",
)
@click.option(
    "--to-dot",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to indicate that the executions should be presented as a graph.",
)
@click.option(
    "--render-dot",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to indicate that the executions should be presented as a graph.",
)
@click.option(
    "--to-png",
    required=False,
    is_flag=True,
    default=False,
    help="Flag to indicate that the executions should be presented as a graph.",
)
@click.pass_obj
def list_index(obj, as_graph, to_dot, render_dot, to_png):
    """Show the workbench executions."""
    aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Graph visualization", 1)

    workbench = obj["workbench"]
    graph_manager = workbench.session.index.graph_manager

    if not graph_manager.is_empty:
        if as_graph:
            aesthetic_print("[bold]Execution graph[bold]", 0)

            filename = workbench.config.tool.storm.name.strip().lower()
            if to_dot or render_dot:
                plot_dot_indexed_executions(
                    graph_manager, filename=f"{filename}.dot", render=render_dot
                )

            if to_png:
                plot_styled_indexed_executions(
                    graph_manager, filename=f"{filename}.png"
                )

            if not any([to_dot, to_png]):
                show_ascii_graph(graph_manager.graph)
        else:
            show_table_execution_index_status(graph_manager.to_frame())
    else:
        aesthetic_print("Graph empty!", 0)

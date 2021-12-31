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

from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.graph import show_ascii_graph
from storm_workbench.cli.graphics.table import show_table_execution_index_status
from storm_workbench.workbench import Workbench


@click.group(name="index")
@click.pass_context
def index(ctx):
    """Execution index management."""
    if ctx.obj is None:
        ctx.obj = dict()

    try:
        ctx.obj["workbench"] = Workbench()
    except:
        aesthetic_traceback(show_locals=True)

        exit()


@index.command(name="list")
@click.option(
    "--as-graph",
    required=False,
    is_flag=True,
    default=False,
    help="Flag indicating that the execution index should be "
    "presented as a Directed Acyclic Graph (DAG) in the terminal.",
)
@click.option(
    "--to-dot",
    required=False,
    is_flag=True,
    default=False,
    help="Flag indicating that the execution Directed Acyclic Graph (DAG) "
    "should be saved in a ``dot`` file (Require ``--as-graph`` flag).",
)
@click.option(
    "--render-dot",
    required=False,
    is_flag=True,
    default=False,
    help="Flag indicating that the execution Directed Acyclic Graph (DAG) "
    "should be rendered in a ``png`` file based on a ``dot`` file (Require "
    "``--as-graph`` flag).",
)
@click.option(
    "--to-png",
    required=False,
    is_flag=True,
    default=False,
    help="Flag indicating that the execution Directed Acyclic Graph (DAG) "
    "should be rendered in a ``png`` file based on a ``igraph.plotting`` "
    "module (Require ``--as-graph`` flag).",
)
@click.pass_obj
def list_index(obj, as_graph, to_dot, render_dot, to_png):
    """List the Workbench indexed executions."""
    aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Executions :sparkles:", 1)

    workbench = obj["workbench"]
    graph_manager = workbench.session.index.graph_manager

    try:
        if not graph_manager.is_empty:
            if as_graph:
                aesthetic_print("[bold]Executions as DAG[bold]", 0)

                filename = workbench.config.tool.storm.name.strip().lower()
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
                show_table_execution_index_status(graph_manager.to_frame())
        else:
            aesthetic_print("There is no indexed execution in this Workbench!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@index.command(name="rm")
@click.argument("execution-id", required=True, nargs=-1)
@click.option(
    "--remove-related",
    required=False,
    is_flag=True,
    help="Flag indicating if the executions related to the execution "
    "that will be removed should be removed too.",
    default=True,
)
@click.pass_obj
def rm_index_obj(obj, execution_id, remove_related):
    """Remove an indexed execution."""
    remove = click.confirm(
        f"This command will remove the execution {execution_id}. Are you sure you want to continue ?",
        abort=True,
    )

    if remove:
        try:
            workbench = obj["workbench"]
            workbench.session.index.deindex_execution(execution_id[0], remove_related)

            workbench.session.save_session()
            aesthetic_print("Execution removed!", 0)
        except:
            aesthetic_traceback(show_locals=True)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

import click
import rich.markdown

from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.exceptions import InvalidCommand
from storm_workbench.workbench import Workbench


@click.group(name="exec")
@click.pass_context
def exec_(ctx):
    """Create and use Reproducible Research."""
    if ctx.obj is None:
        ctx.obj = dict()

    try:
        ctx.obj["workbench"] = Workbench()
    except:
        aesthetic_traceback(show_locals=True)
        exit()


@exec_.command(name="run")
@click.argument("command", required=False, nargs=-1)
@click.option(
    "-n",
    "--name",
    type=str,
    required=False,
    help="Execution name identifier.",
)
@click.option(
    "-d",
    "--description",
    type=str,
    required=False,
    help="Execution description.",
)
@click.option(
    "-sf",
    "--stormfile",
    required=False,
    type=click.Path(
        exists=True,
        resolve_path=True,
        path_type=Path,
        dir_okay=False,
        file_okay=True,
    ),
    help="Stormfile with the processing Pipeline definition.",
)
@click.pass_obj
def exec_run(obj, command=None, name=None, description=None, stormfile=None):
    """Execute an experiment in a reproducible way.

    When the execution is done by the `Storm Workbench`, all computational components used on the execution will be
    registered transparently. With this, after the execution, the experiment can be reproduced without many efforts.
    For example, if you want to run a python script and then reproduce it, you can use `Storm Workbench` to help you.

    To do this, the execution that is normally done like this:

       $ python3 myscript.py

    with the Storm Workbench will look like this:

       $ workbench exec run python3 myscript.py

    The main difference here is that now, the execution is controlled by `Storm Workbench`, which allows you to extract
    information from the execution and save all the elements needed to reproduce the execution.

    This command was created using the ReproZip tool. Many thanks to the ReproZip team.
    """
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Reproducible Execution :arrows_counterclockwise:"
    )

    if type(stormfile) == bytes:
        stormfile = Path(stormfile.decode())

    try:
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Running...", 0)

        workbench = obj["workbench"]
        workbench.stage.operation.execution.run(
            name=name, description=description, command=command, stormfile=stormfile
        )

        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Finished!", 0)

    except InvalidCommand as error:
        aesthetic_print("[bold red]Storm Workbench[/bold red]: Problems founded", 0)
        aesthetic_print(rich.markdown.Markdown(str(error)), 0)

    except RuntimeError as error:
        aesthetic_print("[bold red]Storm Workbench[/bold red]: Problems founded", 0)
        aesthetic_print(rich.markdown.Markdown(str(error)))

    except:
        aesthetic_traceback(show_locals=True)


@exec_.command(name="update")
@click.pass_obj
def update(obj):
    """Re-execute the Execution Compendia outdated.

    This command identifies and re-executes all outdated Execution Compendia, which is useful when multiple runs need
    to be updated because of changing results from other scripts. An execution is considered outdated when any of its
    predecessors have a run performed after its creation.

    For example, below we have three associated executions:

         *(Execution 1) -> *(Execution 2) -> *(Execution 3)

    All are up-to-date. If the `Execution 2` is executed again, all its subsequent ones will
    be out of date since they depend on the result generated by this Execution. Following this rule, in this
    example, the `Execution 3` is outdated.
    """
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Reproducible Execution (Update mode) :leftwards_arrow_with_hook:"
    )

    try:
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Running...", 0)

        workbench = obj["workbench"]
        workbench.stage.operation.execution.update()

        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Finished!", 0)

    except:
        aesthetic_traceback(show_locals=True)


@exec_.command(name="rerun")
@click.option(
    "-f",
    "--required-files-reference",
    required=False,
    type=click.Path(exists=True, resolve_path=True, dir_okay=False, file_okay=True),
    help="JSON file with the reference (Path and Checksum) files required to reproduce the experiment.",
)
@click.option(
    "-e",
    "--env",
    required=False,
    multiple=True,
    help="Environment variable required to reproduce the experiment (Multiple values allowed).",
)
@click.pass_obj
def rerun(obj, required_files_reference, env):
    """Reproduce a previous generated experiment."""
    aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Reproduction :repeat:")

    try:
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Running...", 0)

        workbench = obj["workbench"]
        workbench.stage.operation.reexecution.run(required_files_reference, env)

        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Finished!", 0)

    except:
        aesthetic_traceback(show_locals=True)


def register_command(ctx):
    """Register the command in a context."""
    ctx.add_command(exec_)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import shutil
from pathlib import Path

import click
import rich.markdown
from storm_core.helper.exporter import BagItExporter

from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.constants import WorkbenchDefinitions
from storm_workbench.workbench import Workbench


@click.group(name="env")
@click.pass_context
def env(ctx):
    """Workbench environment management."""
    if ctx.obj is None:
        ctx.obj = dict()

    try:
        ctx.obj["workbench"] = Workbench()
    except:
        aesthetic_traceback(show_locals=True)

        exit()


@env.command(name="get")
@click.pass_obj
def get_env(obj):
    """Get the current workbench environment description."""
    workbench = obj["workbench"]
    current_storage = workbench.config.tool.storm.storage

    aesthetic_print(f"Current storage ID: {current_storage.name}", 0)
    aesthetic_print(f"Complete path: {current_storage}", 0)


@env.command(name="clean")
@click.pass_obj
def clean_env(obj):
    """Cleanup the Workbench environment.

    This command will remove all execution registered
    (files and metadata) from the current workbench
    environment."""
    remove = click.confirm(
        "This command will remove all execution registered "
        "(files and metadata) from the current workbench "
        "environment. Are you sure you want to continue ?",
        abort=True,
    )

    if remove:
        try:
            workbench = obj["workbench"]
            current_storage = workbench.config.tool.storm.storage

            shutil.rmtree(current_storage)
            aesthetic_print("Storage cleaned!", 0)
        except:
            aesthetic_traceback(show_locals=True)


@env.command(name="export")
@click.option(
    "-o",
    "--output-dir",
    required=True,
    help="Directory where the exported package will be saved.",
    type=click.Path(
        exists=False, resolve_path=True, path_type=Path, dir_okay=True, file_okay=False
    ),
)
@click.option(
    "-p",
    "--processes",
    required=False,
    type=int,
    default=2,
    help="Number of processes used to calculate the package files checksum during the export.",
)
def export_env(output_dir, processes):
    """Export the workbench compendium package.

    Export the all current workbench execution (files and metadata). The
    generated package can be used to reproduce the complete experiment
    registered.
    """
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Compendium package export :package:", 1
    )

    workbench = Workbench()
    if workbench.session.index.graph_manager.is_outdated:
        aesthetic_print(
            "[bold red]Storm Workbench[/bold red]: Problems founded :disappointed_relieved:",
            0,
        )
        aesthetic_print(
            rich.markdown.Markdown(
                "Some commands are **outdated**! Update them to export the compendium."
            ),
            0,
        )

        return

    if workbench.session.index.graph_manager.is_empty:
        aesthetic_print("There is no indexed execution in this Workbench!", 0)

        return

    # Exporting!
    aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Exporting :mage:", 1)
    try:
        # copying the workbench definition file
        # to the storage directory.
        tmp_definition_file = (
            workbench.config.tool.storm.storage
            / WorkbenchDefinitions.WB_DEFINITION_FILE
        )
        shutil.copy(
            workbench.config.tool.storm.definition_file,
            tmp_definition_file,
        )

        BagItExporter.save(
            workbench.config.tool.storm.storage,
            output_dir / workbench.config.tool.storm.name,
            processes=processes,
        )

        tmp_definition_file.unlink()
    except:
        aesthetic_traceback(show_locals=True)

    aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Done!", 0)

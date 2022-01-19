# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click

from storm_workbench.cli.graphics.aesthetic import aesthetic_traceback, aesthetic_print
from storm_workbench.workbench import Workbench


@click.group(name="export")
@click.pass_context
def export(ctx):
    """Create sharable and reusable Compendia and Datasets."""
    if ctx.obj is None:
        ctx.obj = dict()

    try:
        ctx.obj["workbench"] = Workbench()
    except:
        aesthetic_traceback(show_locals=True)
        exit()


@export.command(name="compendium")
@click.option(
    "-o",
    "--output-dir",
    required=True,
    type=click.Path(
        exists=False,
        resolve_path=True,
        dir_okay=True,
        file_okay=False,
    ),
    help="Output directory.",
)
@click.option(
    "-t",
    "--temporary-dir",
    required=False,
    default=None,
    type=click.Path(
        exists=False,
        resolve_path=True,
        dir_okay=True,
        file_okay=False,
    ),
    help="Temporary directory used as a exchange directory to read/write files (Default is /tmp).",
)
@click.option(
    "-f",
    "--filename",
    required=False,
    default=None,
    help="Exported file name (Default is the Workbench name).",
)
@click.pass_obj
def export_compendia(obj, output_dir=None, temporary_dir=None, filename=None):
    """Export all Workbench Execution Compendia."""
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Compendia Package Export :package:", 0
    )

    try:
        workbench = obj["workbench"]

        # getting the available compendia to export.
        execution_compendia = workbench.backstage.execution.index.search.query.query()

        # saving the compendia
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Exporting...", 0)

        output_file = workbench.stage.exporter.compendium.save(
            compendia=execution_compendia,
            output_dir=output_dir,
            temp_dir=temporary_dir,
            filename=filename,
        )

        aesthetic_print(
            f"[bold cyan]Storm Workbench[/bold cyan]: Package exported to {output_file}"
        )

        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Finished!", 0)

    except:
        aesthetic_traceback(show_locals=True)


@export.command(name="dataset")
@click.option(
    "-o",
    "--output-dir",
    required=True,
    type=click.Path(
        exists=False,
        resolve_path=True,
        dir_okay=True,
        file_okay=False,
    ),
    help="Output directory.",
)
@click.option(
    "-t",
    "--temporary-dir",
    required=False,
    default=None,
    type=click.Path(
        exists=False,
        resolve_path=True,
        dir_okay=True,
        file_okay=False,
    ),
    help="Temporary directory used as a exchange directory to read/write files (Default is /tmp).",
)
@click.option(
    "-f",
    "--filename",
    required=False,
    default=None,
    help="Exported file name (Default is the Workbench name).",
)
@click.pass_obj
def export_dataset(obj, output_dir=None, temporary_dir=None, filename=None):
    """Export Workbench Execution Compendia Unpackaged files."""
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Compendia Dataset Export :card_file_box:",
        0,
    )

    try:
        workbench = obj["workbench"]

        # getting the available compendia to export their input (and unpacked) data.
        execution_compendia = workbench.backstage.execution.index.search.query.query()

        # saving the dataset
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Exporting...", 0)

        output_file = workbench.stage.exporter.dataset.save(
            compendia=execution_compendia,
            output_dir=output_dir,
            temp_dir=temporary_dir,
            filename=filename,
        )

        aesthetic_print(
            f"[bold cyan]Storm Workbench[/bold cyan]: Dataset exported to {output_file}"
        )

        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Finished!", 0)

    except:
        aesthetic_traceback(show_locals=True)


def register_command(ctx):
    """Register the command in a context."""
    ctx.add_command(export)

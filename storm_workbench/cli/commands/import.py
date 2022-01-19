# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click

from storm_workbench.api.stage.exporter.compendium.service import (
    CompendiumExporterService,
)
from storm_workbench.api.stage.exporter.dataset.service import DatasetExporterService
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback


@click.group(name="import")
@click.pass_context
def import_(ctx):
    """Import Compendia and Datasets."""


@import_.command(name="compendium")
@click.option(
    "-f",
    "--file",
    required=True,
    default=None,
    type=click.Path(
        exists=False,
        resolve_path=True,
        dir_okay=False,
        file_okay=True,
    ),
    help="File to be imported.",
)
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
def import_compendia(file=None, output_dir=None):
    """Import a Workbench Execution Compendia from a file."""
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Compendia Package Import :package:", 0
    )

    try:
        # creating the service object.
        # rework needed: we will improve this class relation to avoid the CLI
        # know how to create a service object.
        standalone_compendium_exporter_service = CompendiumExporterService()

        # loading
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Loading...", 0)

        output_file = standalone_compendium_exporter_service.load(file, output_dir)

        aesthetic_print(
            f"[bold cyan]Storm Workbench[/bold cyan]: Compendia import to {output_file}"
        )
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Finished!", 0)

    except:
        aesthetic_traceback(show_locals=True)


@import_.command(name="dataset")
@click.option(
    "-f",
    "--file",
    required=True,
    default=None,
    type=click.Path(
        exists=False,
        resolve_path=True,
        dir_okay=False,
        file_okay=True,
    ),
    help="File to be imported.",
)
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
def import_dataset(file=None, output_dir=None):
    """Import a Workbench Dataset from a file."""
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Compendia Dataset Import :card_file_box:",
        0,
    )

    try:
        # creating the service object.
        standalone_compendium_exporter_service = DatasetExporterService()

        # loading
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Loading...", 0)

        output_file = standalone_compendium_exporter_service.load(file, output_dir)

        aesthetic_print(
            f"[bold cyan]Storm Workbench[/bold cyan]: Dataset import to {output_file}"
        )
        aesthetic_print("[bold cyan]Storm Workbench[/bold cyan]: Finished!", 0)

    except:
        aesthetic_traceback(show_locals=True)


def register_command(ctx):
    """Register the command in a context."""
    ctx.add_command(import_)

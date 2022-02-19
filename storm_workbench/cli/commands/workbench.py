# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

import click

from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.template import write_template
from storm_workbench.workbench.settings import (
    find_workbench_definition_file,
    find_secrets_file,
)

from storm_workbench import constants


@click.command(name="init")
def init():
    """Initialize a new Workbench."""
    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Workbench initialization", 1
    )

    gretting_message = """
    Welcome to [bold cyan]Storm Workbench[/bold cyan]. This tool aims to enhance the reproducibility
    of scientific experiments performed with different programming languages and computational resources.

    This program is in an [bold red]experimental[/bold red] stage, so if you find any problems,
    please report them and help us to improve this tool. To contact us, you can use the following links:
        - [bold]Github[/bold]: [blue]https://github.com/storm-platform/storm-workbench[/blue];
        - [bold]Issues[/bold]: [blue]https://github.com/storm-platform/storm-workbench/issues[/blue].

    Now, let's get to creating your workbench...
    """
    aesthetic_print(gretting_message, 2)

    secrets_file = None
    workbench_file = None

    overwrite_secrets = True
    overwrite_workbench = True

    try:
        workbench_file = find_workbench_definition_file()

        overwrite_workbench = click.confirm(
            f"Existing Workbench found!  Do you want to go ahead and "
            f"create a new definition file? (This will overwrite the "
            f"current configuration)",
            abort=False,
        )
    except:
        workbench_file = Path.cwd() / constants.WB_DEFINITION_FILE

    # finding for a secret files
    secrets_file = find_secrets_file()

    if secrets_file:
        overwrite_secrets = click.confirm(
            f"Existing `.secrets` found!  Do you want to go ahead and "
            f"create a new `.secrets` file? (This will overwrite the "
            f"current configuration)",
            abort=False,
        )
    else:
        secrets_file = Path.cwd() / constants.WB_SECRETS_FILE

    if overwrite_workbench:
        try:
            aesthetic_print(
                "[bold cyan]Storm Workbench[/bold cyan]: Creating a new workbench definition file.",
                0,
            )
            workbench_name = click.prompt("Please enter the Workbench name", type=str)

            # rendering the workbench definition template.
            write_template(
                workbench_file, "config/workbench.toml", workbench_name=workbench_name
            )

        except:
            aesthetic_traceback(show_locals=True)

    if overwrite_secrets:
        aesthetic_print(
            "[bold cyan]Storm Workbench[/bold cyan]: Creating the `.secrets.toml` file.",
            0,
        )

        write_template(secrets_file, "config/secrets.toml")

    aesthetic_print(
        "[bold cyan]Storm Workbench[/bold cyan]: Workbench is configured!.",
        0,
    )


def register_command(ctx):
    """Register the command in a context."""
    ctx.add_command(init)

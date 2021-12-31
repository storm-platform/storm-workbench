# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

import click
import tomlkit as toml
from pkg_resources import resource_string

from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback


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

    create = True
    workbench_definition_file = Path.cwd() / "workbench.toml"

    if workbench_definition_file.exists():
        aesthetic_print(
            "[bold red]Storm Workbench[/bold red]: Problems founded :disappointed_relieved:",
            0,
        )
        create = click.confirm(
            "You already have a workbench defined in this directory. Do you "
            "want to continue? Your Workbench settings will be removed but the "
            "references of the runs will be kept",
            abort=True,
        )

    if create:
        try:
            aesthetic_print(
                "[bold cyan]Storm Workbench[/bold cyan]: Creating a new workbench definition file.",
                0,
            )
            workbench_name = click.prompt("Please enter the Workbench name", type=str)

            # loading the workbench definition template.
            workbench_definition_template = resource_string(
                __name__, "templates/workbench.toml"
            )

            # populate the template.
            workbench_definition = toml.loads(
                workbench_definition_template.decode("utf-8")
            )
            workbench_definition["tool"]["storm"]["name"] = workbench_name

            # saving the workbench definition file.
            toml.dump(workbench_definition, workbench_definition_file.open("w"))
            aesthetic_print(
                "[bold cyan]Storm Workbench[/bold cyan]: Done!",
                0,
            )
        except:
            aesthetic_traceback(show_locals=True)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json
from pathlib import Path

import click
import rich.markdown
from storm_client.models.project import Project

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.table import aesthetic_table_by_document
from storm_workbench.cli.graphics.tree import aesthetic_tree_base


@service.group(name="project")
def project():
    """Project management."""


@project.command(name="describe")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Project identifier.",
)
@click.pass_obj
def project_describe(obj, id):
    """Get a project description."""
    workbench = obj["workbench"]

    try:
        project_description = workbench.stage.ws.project.describe(id)
        aesthetic_print(project_description)

    except:
        aesthetic_traceback(show_locals=True)


@project.command(name="finish")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Project identifier.",
)
@click.pass_obj
def project_finish(obj, id):
    """Finish a Storm WS Project."""
    workbench = obj["workbench"]

    try:
        project_finished = workbench.stage.ws.project.finish(id)

        tree = aesthetic_tree_base(
            title="\n[bold]Project - Finish[/bold]",
            children=[
                f"[blue]Project ID[/blue]: {project_finished.id}",
                f"[blue]Status[/blue]: [green]Finished[/green]",
            ],
        )
        aesthetic_print(tree)

    except:
        aesthetic_traceback(show_locals=True)


@project.command(name="create")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Project Identifier.",
)
@click.option(
    "--title",
    required=False,
    type=str,
    help="Project title.",
)
@click.option(
    "--description",
    required=False,
    type=str,
    help="Project description.",
)
@click.option(
    "-m",
    "--metadata-file",
    required=False,
    type=click.Path(
        exists=True,
        resolve_path=True,
        dir_okay=False,
        file_okay=True,
    ),
    help="Metadata JSON file.",
)
@click.pass_obj
def project_create(obj, id=None, title=None, description=None, metadata_file=None):
    """Create a new Project."""
    workbench = obj["workbench"]

    # defining the metadata
    metadata = None

    if metadata_file:
        with Path(metadata_file).open(mode="r") as ifile:
            metadata = json.load(ifile)

    elif all([title, description]):
        metadata = dict(title=title, description=description)

    else:
        aesthetic_print(
            rich.markdown.Markdown(
                "To create a Project, you need to define the `--title` and "
                "`--description` options or set the `--metadata-file`"
            )
        )
        return

    try:
        # creating the project.
        project = Project(id=id, metadata=metadata)
        project_created = workbench.stage.ws.project.create(project)

        tree = aesthetic_tree_base(
            title="\n[bold]Project - Create[/bold]",
            children=[
                f"[blue]Project ID[/blue]: {project_created.id}",
                f"[blue]Status[/blue]: [green]Created[/green]",
            ],
        )
        aesthetic_print(tree)

    except:
        aesthetic_traceback(show_locals=True)


@project.command(name="search")
@click.option(
    "--query",
    required=False,
    default=None,
    type=str,
    help="Search query used to filter results based on ElasticSearch's query string syntax.",
)
@click.option(
    "--user-project-only",
    required=False,
    default=False,
    is_flag=True,
    type=bool,
    help="Flag indicating if the search should be made only in the User context, where "
    "all Project created by the user will be available.",
)
@click.pass_obj
def project_search(obj, query=None, user_project_only=None):
    """Search Storm WS projects."""
    workbench = obj["workbench"]

    try:
        project_search_result = workbench.stage.ws.project.search(
            user_records=user_project_only, q=query
        )

        if project_search_result:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Title": "metadata.title",
                "Description": "metadata.description",
                "Finished": "is_finished",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Projects", table_declaration, project_search_result
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)

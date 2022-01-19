# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from storm_client.models.pipeline import Pipeline

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.table import aesthetic_table_by_document
from storm_workbench.cli.graphics.tree import aesthetic_tree_base


@service.group(name="pipeline")
def pipeline():
    """Pipeline management."""


@pipeline.command(name="describe")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Compendium identifier.",
)
@click.pass_obj
def pipeline_describe(obj, id=None):
    """Get a Pipeline description."""
    workbench = obj["workbench"]

    try:
        compendium_description = workbench.stage.ws.pipeline.describe(id)
        aesthetic_print(compendium_description)

    except:
        aesthetic_traceback(show_locals=True)


@pipeline.command(name="finish")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Pipeline identifier.",
)
@click.pass_obj
def pipeline_finish(obj, id):
    """Finish a Storm WS Pipeline."""
    workbench = obj["workbench"]

    try:
        pipeline_finished = workbench.stage.ws.pipeline.finish(id)

        tree = aesthetic_tree_base(
            title="\n[bold]Pipeline - Finish[/bold]",
            children=[
                f"[blue]Project ID[/blue]: {pipeline_finished.id}",
                f"[blue]Status[/blue]: [green]Finished[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@pipeline.command(name="create")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Pipeline Identifier.",
)
@click.option(
    "--title",
    required=True,
    type=str,
    help="Pipeline title.",
)
@click.option(
    "--description",
    required=True,
    type=str,
    help="Pipeline description.",
)
@click.option(
    "--version",
    required=True,
    type=str,
    help="Pipeline Version.",
)
@click.pass_obj
def pipeline_create(obj, id=None, title=None, description=None, version=None):
    """Create a new Pipeline."""
    workbench = obj["workbench"]

    try:
        # creating the pipeline object
        pipeline = Pipeline(
            id=id, metadata=dict(title=title, description=description, version=version)
        )

        pipeline_created = workbench.stage.ws.pipeline.create(pipeline)

        tree = aesthetic_tree_base(
            title="\n[bold]Pipeline - Create[/bold]",
            children=[
                f"[blue]Pipeline ID[/blue]: {pipeline_created.id}",
                f"[blue]Status[/blue]: [green]Created[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@pipeline.command(name="add-compendium")
@click.option(
    "--pipeline-id",
    required=False,
    type=str,
    help="Pipeline Identifier.",
)
@click.option(
    "--compendium-id",
    required=True,
    type=str,
    help="Storm WS Compendium Record identifier (Published).",
)
@click.pass_obj
def pipeline_add_compendium(obj, pipeline_id=None, compendium_id=None):
    """Add a Compendium Record (Published) in the Pipeline."""
    workbench = obj["workbench"]

    try:
        pipeline_updated = workbench.stage.ws.pipeline.add_compendium(
            pipeline_id, compendium_id
        )

        tree = aesthetic_tree_base(
            title="\n[bold]Pipeline - Add Compendium[/bold]",
            children=[
                f"[blue]Pipeline ID[/blue]: {pipeline_updated.id}",
                f"[blue]Status[/blue]: [green]Compendium Added[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@pipeline.command(name="remove-compendium")
@click.option(
    "--pipeline-id",
    required=False,
    type=str,
    help="Pipeline Identifier.",
)
@click.option(
    "--compendium-pid",
    required=True,
    type=str,
    help="Storm WS Compendium Record identifier (Published).",
)
@click.pass_obj
def pipeline_remove_compendium(obj, pipeline_id=None, compendium_pid=None):
    """Remove a Compendium Record from the Pipeline."""
    workbench = obj["workbench"]

    try:
        pipeline_updated = workbench.stage.ws.pipeline.remove_compendium(
            pipeline_id, compendium_pid
        )

        tree = aesthetic_tree_base(
            title="\n[bold]Pipeline - Remove Compendium[/bold]",
            children=[
                f"[blue]Pipeline ID[/blue]: {pipeline_updated.id}",
                f"[blue]Status[/blue]: [green]Compendium Removed[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@pipeline.command(name="search")
@click.option(
    "--query",
    required=False,
    default=None,
    type=str,
    help="Search query used to filter results based on ElasticSearch's query string syntax.",
)
@click.pass_obj
def pipeline_search(obj, query):
    """Search Storm WS Pipelines."""
    workbench = obj["workbench"]

    try:
        pipeline_search_result = workbench.stage.ws.pipeline.search(q=query)

        if pipeline_search_result:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Title": "metadata.title",
                "Description": "metadata.description",
                "Version": "metadata.version",
                "Finished": "is_finished",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Pipelines", table_declaration, pipeline_search_result
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@pipeline.command(name="delete")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Pipeline identifier.",
)
@click.pass_obj
def pipeline_delete(obj, id):
    """Delete a Pipeline from Storm WS."""
    workbench = obj["workbench"]

    remove = click.confirm(
        "This command will delete the Pipeline from the Storm WS. Are you sure you want to continue ?",
        abort=True,
    )

    if remove:
        try:
            workbench.stage.ws.pipeline.delete(id)
            aesthetic_print("[blue]Status[/blue]: [green]Pipeline Deleted[/green]")

        except:
            aesthetic_traceback(show_locals=True)
    else:
        aesthetic_print("Bye")

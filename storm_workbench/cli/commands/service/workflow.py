# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from storm_client.models.workflow import Workflow

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.table import aesthetic_table_by_document
from storm_workbench.cli.graphics.tree import aesthetic_tree_base


@service.group(name="workflow")
def workflow():
    """Workflow management."""


@workflow.command(name="describe")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Compendium identifier.",
)
@click.pass_obj
def workflow_describe(obj, id=None):
    """Get a Workflow description."""
    workbench = obj["workbench"]

    try:
        compendium_description = workbench.stage.ws.workflow.describe(id)
        aesthetic_print(compendium_description)

    except:
        aesthetic_traceback(show_locals=True)


@workflow.command(name="finish")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Workflow identifier.",
)
@click.pass_obj
def workflow_finish(obj, id):
    """Finish a Storm WS Workflow."""
    workbench = obj["workbench"]

    try:
        workflow_finished = workbench.stage.ws.workflow.finish(id)

        tree = aesthetic_tree_base(
            title="\n[bold]Workflow - Finish[/bold]",
            children=[
                f"[blue]Project ID[/blue]: {workflow_finished.id}",
                f"[blue]Status[/blue]: [green]Finished[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@workflow.command(name="create")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Workflow Identifier.",
)
@click.option(
    "--title",
    required=True,
    type=str,
    help="Workflow title.",
)
@click.option(
    "--description",
    required=True,
    type=str,
    help="Workflow description.",
)
@click.option(
    "--version",
    required=True,
    type=str,
    help="Workflow Version.",
)
@click.pass_obj
def workflow_create(obj, id=None, title=None, description=None, version=None):
    """Create a new Workflow."""
    workbench = obj["workbench"]

    try:
        # creating the workflow object
        workflow = Workflow(
            id=id, metadata=dict(title=title, description=description, version=version)
        )

        workflow_created = workbench.stage.ws.workflow.create(workflow)

        tree = aesthetic_tree_base(
            title="\n[bold]Workflow - Create[/bold]",
            children=[
                f"[blue]Workflow ID[/blue]: {workflow_created.id}",
                f"[blue]Status[/blue]: [green]Created[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@workflow.command(name="add-compendium")
@click.option(
    "--workflow-id",
    required=False,
    type=str,
    help="Workflow Identifier.",
)
@click.option(
    "--compendium-id",
    required=True,
    type=str,
    help="Storm WS Compendium Record identifier (Published).",
)
@click.pass_obj
def workflow_add_compendium(obj, workflow_id=None, compendium_id=None):
    """Add a Compendium Record (Published) in the Workflow."""
    workbench = obj["workbench"]

    try:
        workflow_updated = workbench.stage.ws.workflow.add_compendium(
            workflow_id, compendium_id
        )

        tree = aesthetic_tree_base(
            title="\n[bold]Workflow - Add Compendium[/bold]",
            children=[
                f"[blue]Workflow ID[/blue]: {workflow_updated.id}",
                f"[blue]Status[/blue]: [green]Compendium Added[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@workflow.command(name="remove-compendium")
@click.option(
    "--workflow-id",
    required=False,
    type=str,
    help="Workflow Identifier.",
)
@click.option(
    "--compendium-pid",
    required=True,
    type=str,
    help="Storm WS Compendium Record identifier (Published).",
)
@click.pass_obj
def workflow_remove_compendium(obj, workflow_id=None, compendium_pid=None):
    """Remove a Compendium Record from the Workflow."""
    workbench = obj["workbench"]

    try:
        workflow_updated = workbench.stage.ws.workflow.remove_compendium(
            workflow_id, compendium_pid
        )

        tree = aesthetic_tree_base(
            title="\n[bold]Workflow - Remove Compendium[/bold]",
            children=[
                f"[blue]Workflow ID[/blue]: {workflow_updated.id}",
                f"[blue]Status[/blue]: [green]Compendium Removed[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@workflow.command(name="search")
@click.option(
    "--query",
    required=False,
    default=None,
    type=str,
    help="Search query used to filter results based on ElasticSearch's query string syntax.",
)
@click.pass_obj
def workflow_search(obj, query):
    """Search Storm WS Workflow."""
    workbench = obj["workbench"]

    try:
        workflow_search_result = workbench.stage.ws.workflow.search(q=query)

        if workflow_search_result:
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
                "Search result - Workflows", table_declaration, workflow_search_result
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@workflow.command(name="delete")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Workflow identifier.",
)
@click.pass_obj
def workflow_delete(obj, id):
    """Delete a Workflow from Storm WS."""
    workbench = obj["workbench"]

    remove = click.confirm(
        "This command will delete the Workflow from the Storm WS. Are you sure you want to continue ?",
        abort=True,
    )

    if remove:
        try:
            workbench.stage.ws.workflow.delete(id)
            aesthetic_print("[blue]Status[/blue]: [green]Workflow Deleted[/green]")

        except:
            aesthetic_traceback(show_locals=True)
    else:
        aesthetic_print("Bye")

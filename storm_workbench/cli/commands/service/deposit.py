# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from storm_client.models.deposit import DepositJob

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.table import aesthetic_table_by_document
from storm_workbench.cli.graphics.tree import aesthetic_tree_base


@service.group(name="deposit")
def deposit():
    """Deposit Job management."""


@deposit.command(name="describe")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Deposit identifier.",
)
@click.pass_obj
def deposit_describe(obj, id=None):
    """Get a Deposit description."""
    workbench = obj["workbench"]

    try:
        deposit_description = workbench.stage.ws.deposit.describe(id)
        aesthetic_print(deposit_description, 0)

    except:
        aesthetic_traceback(show_locals=True)


@deposit.command(name="create")
@click.option(
    "--service",
    required=True,
    type=str,
    help="Service where the Storm WS will send the Deposit bundle.",
)
@click.option(
    "--workflow-id",
    required=True,
    multiple=True,
    help="Identifier of the Pipeline witch with will be included in the Deposit bundle.",
)
@click.pass_obj
def deposit_create(obj, service=None, pipeline_id=None):
    """Create a new Deposit."""
    workbench = obj["workbench"]

    try:
        # creating the deposit job object
        deposit_obj = DepositJob(service=service, pipelines=pipeline_id)

        deposit_created = workbench.stage.ws.deposit.create(deposit_obj)

        tree = aesthetic_tree_base(
            title="\n[bold]Deposit - Create[/bold]",
            children=[
                f"[blue]Deposit ID[/blue]: {deposit_created.id}",
                f"[blue]Status[/blue]: [green]Created[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@deposit.command(name="update")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Deposit Identifier.",
)
@click.option(
    "--service",
    required=False,
    type=str,
    help="Service where the Storm WS will send the Deposit bundle.",
)
@click.option(
    "--workflow-id",
    required=False,
    multiple=True,
    help="Identifier of the Pipeline witch with will be included in the Deposit bundle.",
)
@click.pass_obj
def deposit_update(obj, id=None, service=None, pipeline_id=None):
    """Update an existing Storm WS Deposit."""
    workbench = obj["workbench"]

    try:
        # creating the deposit job object
        deposit_obj = DepositJob(id=id, service=service, pipelines=pipeline_id)

        deposit_updated = workbench.stage.ws.deposit.update(deposit_obj)

        tree = aesthetic_tree_base(
            title="\n[bold]Deposit - Update[/bold]",
            children=[
                f"[blue]Deposit ID[/blue]: {deposit_updated.id}",
                f"[blue]Status[/blue]: [green]Updated[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@deposit.command(name="delete")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Deposit identifier.",
)
@click.pass_obj
def deposit_delete(obj, id=None):
    """Delete an existing Storm WS Deposit."""
    workbench = obj["workbench"]

    try:
        workbench.stage.ws.deposit.delete(id)
        aesthetic_print("[blue]Status[/blue]: [green]Deposit Deleted[/green]", 0)

    except:
        aesthetic_traceback(show_locals=True)


@deposit.command(name="services")
@click.pass_obj
def deposit_services(obj):
    """List the available Deposit target services."""
    workbench = obj["workbench"]

    try:
        available_deposit_services = workbench.stage.ws.deposit.services()

        if available_deposit_services:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Title": "metadata.title",
                "Description": "metadata.description",
                "Required Fields": "metadata.required_fields.0.field_name",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Deposit Services",
                table_declaration,
                available_deposit_services,
            )
            aesthetic_print(table, 0)

    except:
        aesthetic_traceback(show_locals=True)


@deposit.command(name="search")
@click.option(
    "--query",
    required=False,
    default=None,
    type=str,
    multiple=False,
    help="Search query used to filter results based on ElasticSearch's query string syntax.",
)
@click.pass_obj
def deposit_search(obj, query):
    """Search Storm WS Deposits."""
    workbench = obj["workbench"]

    try:
        deposit_search_result = workbench.stage.ws.deposit.search(_params=query)

        if deposit_search_result:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Service": "service",
                "Project ID": "project_id",
                "Pipeline ID": "pipelines.0",  # ToDo: Generalize to accept multiple pipelines in the table.
                "Status": "status",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Deposits", table_declaration, deposit_search_result
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@deposit.command(name="start")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Deposit Identifier.",
)
@click.option(
    "--args",
    required=False,
    multiple=True,
    help="Extra arguments to the Deposit Resource (e.g., Used to define arguments like Service Token).",
)
@click.pass_obj
def deposit_start(obj, id=None, args=None):
    """Start an deposit task."""
    workbench = obj["workbench"]

    try:
        deposit_started = workbench.stage.ws.deposit.start(id, _params=",".join(args))

        tree = aesthetic_tree_base(
            title="\n[bold]Deposit task[/bold]",
            children=[
                f"[blue]Deposit ID[/blue]: {deposit_started.id}",
                f"[blue]Status[/blue]: [green]Deposit in progress[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)

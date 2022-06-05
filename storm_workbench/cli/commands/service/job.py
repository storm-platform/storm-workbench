# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from storm_client.models.execution import ExecutionJob

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.table import aesthetic_table_by_document
from storm_workbench.cli.graphics.tree import aesthetic_tree_base


@service.group(name="execution")
def execution_job():
    """Execution Job management."""


@execution_job.command(name="describe")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Execution Job identifier.",
)
@click.pass_obj
def execution_job_describe(obj, id=None):
    """Get a ExecutionJob description."""
    workbench = obj["workbench"]

    try:
        job_description = workbench.stage.ws.execution.describe(id)
        aesthetic_print(job_description, 0)

    except:
        aesthetic_traceback(show_locals=True)


@execution_job.command(name="create")
@click.option(
    "--workflow-id",
    required=True,
    type=str,
    help="Workflow Identifier.",
)
@click.option(
    "--service",
    required=True,
    type=str,
    help="Service used to execute the Execution Job.",
)
@click.pass_obj
def execution_job_create(obj, workflow_id=None, service=None):
    """Create a new ExecutionJob."""
    workbench = obj["workbench"]

    try:
        # creating the execution object
        execution_job_obj = ExecutionJob(workflow_id=workflow_id, service=service)

        execution_job_created = workbench.stage.ws.execution.create(execution_job_obj)

        tree = aesthetic_tree_base(
            title="\n[bold]Execution Job - Create[/bold]",
            children=[
                f"[blue]Execution Job ID[/blue]: {execution_job_created.id}",
                f"[blue]Status[/blue]: [green]Created[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@execution_job.command(name="update")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Execution Job Identifier.",
)
@click.option(
    "--workflow-id",
    required=False,
    type=str,
    help="Workflow Identifier.",
)
@click.option(
    "--service",
    required=False,
    type=str,
    help="Service used to execute the Execution Job.",
)
@click.pass_obj
def execution_job_update(obj, id=None, workflow_id=None, service=None):
    """Update an existing Storm WS Execution Job."""
    workbench = obj["workbench"]

    try:
        # creating the execution object.
        execution_job_obj = ExecutionJob(id=id, workflow_id=workflow_id, service=service)

        execution_job_updated = workbench.stage.ws.execution.update(execution_job_obj)

        tree = aesthetic_tree_base(
            title="\n[bold]Execution Job - Update[/bold]",
            children=[
                f"[blue]Execution Job ID[/blue]: {execution_job_updated.id}",
                f"[blue]Status[/blue]: [green]Updated[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@execution_job.command(name="delete")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Execution Job identifier.",
)
@click.pass_obj
def execution_job_delete(obj, id=None):
    """Delete an existing Storm WS Job."""
    workbench = obj["workbench"]

    try:
        workbench.stage.ws.execution.delete(id)
        aesthetic_print("[blue]Status[/blue]: [green]Execution Job Deleted[/green]", 0)

    except:
        aesthetic_traceback(show_locals=True)


@execution_job.command(name="services")
@click.pass_obj
def execution_job_services(obj):
    """List the available execution job services."""
    workbench = obj["workbench"]

    try:
        available_execution_services = workbench.stage.ws.execution.services()

        if available_execution_services:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Title": "metadata.title",
                "Description": "metadata.description",
                # special case: in the current storm platform version,
                # all services require only one field. In the future, this
                # may be change to support multiple fields.
                "Required Fields": "metadata.required_fields.0.field_name",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Execution Job Services",
                table_declaration,
                available_execution_services,
            )
            aesthetic_print(table, 0)

    except:
        aesthetic_traceback(show_locals=True)


@execution_job.command(name="search")
@click.option(
    "--query",
    required=False,
    default=None,
    type=str,
    help="Search query used to filter results based on ElasticSearch's query string syntax.",
)
@click.pass_obj
def execution_job_search(obj, query):
    """Search Storm WS Jobs."""
    workbench = obj["workbench"]

    try:
        job_search_result = workbench.stage.ws.execution.search(_params=query)

        if job_search_result:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Service": "service",
                "Project ID": "project_id",
                "Workflow ID": "workflow_id",
                "Status": "status",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Execution Jobs", table_declaration, job_search_result
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@execution_job.command(name="start")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Workflow Identifier.",
)
@click.option(
    "--args",
    required=False,
    multiple=True,
    help="Extra arguments to the Execution Job Resource (e.g., Used to define arguments like Service Token).",
)
@click.pass_obj
def execution_job_start(obj, id=None, args=None):
    """Start the execution of an existing Job."""
    workbench = obj["workbench"]

    try:
        execution_job_started = workbench.stage.ws.execution.start(id, _params=",".join(args))

        tree = aesthetic_tree_base(
            title="\n[bold]Execution Job - Execution[/bold]",
            children=[
                f"[blue]Execution Job ID[/blue]: {execution_job_started.id}",
                f"[blue]Status[/blue]: [green]Execution started[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)

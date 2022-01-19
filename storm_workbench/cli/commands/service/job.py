# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from storm_client.models.job import Job

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.table import aesthetic_table_by_document
from storm_workbench.cli.graphics.tree import aesthetic_tree_base


@service.group(name="job")
def job():
    """Job Execution management."""


@job.command(name="describe")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Job identifier.",
)
@click.pass_obj
def job_describe(obj, id=None):
    """Get a Job description."""
    workbench = obj["workbench"]

    try:
        job_description = workbench.stage.ws.job.describe(id)
        aesthetic_print(job_description, 0)

    except:
        aesthetic_traceback(show_locals=True)


@job.command(name="create")
@click.option(
    "--pipeline-id",
    required=True,
    type=str,
    help="Pipeline Identifier.",
)
@click.option(
    "--service",
    required=True,
    type=str,
    help="Service used to execute the Job.",
)
@click.pass_obj
def job_create(obj, pipeline_id=None, service=None):
    """Create a new Job."""
    workbench = obj["workbench"]

    try:
        # creating the job object
        job_obj = Job(pipeline_id=pipeline_id, service=service)

        job_created = workbench.stage.ws.job.create(job_obj)

        tree = aesthetic_tree_base(
            title="\n[bold]Job - Create[/bold]",
            children=[
                f"[blue]Job ID[/blue]: {job_created.id}",
                f"[blue]Status[/blue]: [green]Created[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@job.command(name="update")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Job Identifier.",
)
@click.option(
    "--pipeline-id",
    required=False,
    type=str,
    help="Pipeline Identifier.",
)
@click.option(
    "--service",
    required=False,
    type=str,
    help="Service used to execute the Job.",
)
@click.pass_obj
def job_update(obj, id=None, pipeline_id=None, service=None):
    """Update an existing Storm WS Job."""
    workbench = obj["workbench"]

    try:
        # creating the job object.
        job_obj = Job(id=id, pipeline_id=pipeline_id, service=service)

        job_updated = workbench.stage.ws.job.update(job_obj)

        tree = aesthetic_tree_base(
            title="\n[bold]Job - Update[/bold]",
            children=[
                f"[blue]Job ID[/blue]: {job_updated.id}",
                f"[blue]Status[/blue]: [green]Updated[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)


@job.command(name="delete")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Job identifier.",
)
@click.pass_obj
def job_delete(obj, id=None):
    """Delete an existing Storm WS Job."""
    workbench = obj["workbench"]

    try:
        workbench.stage.ws.job.delete(id)
        aesthetic_print("[blue]Status[/blue]: [green]Job Deleted[/green]", 0)

    except:
        aesthetic_traceback(show_locals=True)


@job.command(name="services")
@click.pass_obj
def job_services(obj):
    """List the available job execution services."""
    workbench = obj["workbench"]

    try:
        available_execution_services = workbench.stage.ws.job.services()

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
                "Search result - Job Execution Services",
                table_declaration,
                available_execution_services,
            )
            aesthetic_print(table, 0)

    except:
        aesthetic_traceback(show_locals=True)


@job.command(name="search")
@click.option(
    "--query",
    required=False,
    default=None,
    type=str,
    help="Search query used to filter results based on ElasticSearch's query string syntax.",
)
@click.pass_obj
def job_search(obj, query):
    """Search Storm WS Jobs."""
    workbench = obj["workbench"]

    try:
        job_search_result = workbench.stage.ws.job.search(_params=query)

        if job_search_result:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Service": "service",
                "Project ID": "project_id",
                "Pipeline ID": "pipeline_id",
                "Status": "status",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Jobs", table_declaration, job_search_result
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@job.command(name="start")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Pipeline Identifier.",
)
@click.option(
    "--args",
    required=False,
    multiple=True,
    help="Extra arguments to the Job Resource (e.g., Used to define arguments like Service Token).",
)
@click.pass_obj
def job_start(obj, id=None, args=None):
    """Start the execution of an existing Job."""
    workbench = obj["workbench"]

    try:
        job_started = workbench.stage.ws.job.start(id, _params=",".join(args))

        tree = aesthetic_tree_base(
            title="\n[bold]Job - Execution[/bold]",
            children=[
                f"[blue]Job ID[/blue]: {job_started.id}",
                f"[blue]Status[/blue]: [green]Execution started[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except:
        aesthetic_traceback(show_locals=True)

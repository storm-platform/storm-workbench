# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
import rich.markdown

from storm_workbench.cli.commands.service.service import service
from storm_workbench.cli.graphics.aesthetic import aesthetic_print, aesthetic_traceback
from storm_workbench.cli.graphics.table import aesthetic_table_by_document
from storm_workbench.cli.graphics.tree import aesthetic_tree_base
from storm_workbench.exceptions import ExecutionCompendiumNotFound


@service.group(name="compendium")
def compendium():
    """Compendium management."""


@compendium.command(name="describe")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Compendium identifier.",
)
@click.option(
    "--draft",
    required=False,
    default=False,
    is_flag=True,
    type=bool,
    help="Flag indicating if the compendium to describe is a Draft.",
)
@click.pass_obj
def compendium_describe(obj, id=None, draft=False):
    """Get a compendium description."""
    workbench = obj["workbench"]

    try:
        compendium_description = workbench.stage.ws.compendium.describe(
            id, is_draft=draft
        )
        aesthetic_print(compendium_description, 0)

    except ExecutionCompendiumNotFound:
        aesthetic_print(
            rich.markdown.Markdown("The defined Execution Compendium was not founded!"),
            0,
        )

    except:
        aesthetic_traceback(show_locals=True)


@compendium.command(name="search")
@click.option(
    "--query",
    required=False,
    default=None,
    type=str,
    help="Search query used to filter results based on ElasticSearch's query string syntax.",
)
@click.option(
    "--user-compendia-only",
    required=False,
    default=False,
    is_flag=True,
    type=bool,
    help="Flag indicating if the search should be made only in the User context, where "
    "all compendia produced by the user will be available (Record and Draft).",
)
@click.pass_obj
def compendium_search(obj, query, user_compendia_only):
    """Search Storm WS Compendia."""
    workbench = obj["workbench"]

    try:
        compendium_search_result = workbench.stage.ws.compendium.search(
            user_records=user_compendia_only, q=query
        )

        if compendium_search_result:
            # declaring the table structure:
            table_declaration = {
                "ID": "id",
                "Title": "metadata.title",
                "Description": "metadata.description",
                "Revision": "revision_id",
                "Published": "is_published",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Compendia", table_declaration, compendium_search_result
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)


@compendium.command(name="draft-new")
@click.option(
    "--source",
    required=True,
    type=str,
    help="Execution Compendium identifier from where the Draft will be created.",
)
@click.pass_obj
def compendium_new_draft(obj, source=None):
    """Create a new Storm WS Compendium Draft from an Execution Compendium."""
    workbench = obj["workbench"]

    try:
        compendium_draft_description = workbench.stage.ws.compendium.new_draft(source)

        tree = aesthetic_tree_base(
            title="\n[bold]Compenium Draft - Create[/bold]",
            children=[
                f"[blue]Compendium ID[/blue]: {compendium_draft_description.id}",
                f"[blue]Status[/blue]: [green]Created[/green]",
            ],
        )
        aesthetic_print(tree, 0)

    except ExecutionCompendiumNotFound:
        aesthetic_print(
            rich.markdown.Markdown("The defined Execution Compendium was not founded!")
        )

    except:
        aesthetic_traceback(show_locals=True)


@compendium.command(name="draft-publish")
@click.option(
    "--id",
    required=False,
    type=str,
    help="Storm WS Compendium Draft identifier.",
)
@click.pass_obj
def compendium_publish(obj, id=None):
    """Publish a Storm WS Compendium Draft.

    This method make a Storm WS Compendium Draft available in the Project. The publication can
    be made with the Workbench Execution Compendium Name or the Storm WS Compendium Draft PID.
    """
    workbench = obj["workbench"]

    try:
        compendium_record_description = workbench.stage.ws.compendium.publish_draft(id)

        tree = aesthetic_tree_base(
            title="\n[bold]Compenium Draft - Publish[/bold]",
            children=[
                f"[blue]Compendium ID (Record)[/blue]: {compendium_record_description.id}",
                f"[blue]Status[/blue]: [green]Published[/green]",
            ],
        )

        aesthetic_print(tree, 0)

    except ValueError:
        aesthetic_print(
            rich.markdown.Markdown(
                "You need to define a `--execution-compendium-name` or `--draft-pid` "
                "to publish a Draft."
            )
        )

    except ExecutionCompendiumNotFound:
        aesthetic_print(
            rich.markdown.Markdown("The defined Execution Compendium was not founded!")
        )

    except:
        aesthetic_traceback(show_locals=True)


@compendium.command(name="files-upload")
@click.option(
    "--source",
    required=True,
    type=str,
    help="Workbench Execution Compendium identifier linked to a Draft "
    "where the Local files will be uploaded",
)
@click.pass_obj
def compendium_upload_files(obj, source=None):
    """Upload the local Execution Compendium files to a Storm WS Compendium Draft."""
    workbench = obj["workbench"]

    try:
        compendium_draft_description = workbench.stage.ws.compendium.upload_draft_files(
            source
        )

        tree = aesthetic_tree_base(
            title="\n[bold]Compenium Draft Files - Upload[/bold]",
            children=[
                f"[blue]Compendium ID[/blue]: {compendium_draft_description.id}",
                f"[blue]Status[/blue]: [green]Uploaded[/green]",
            ],
        )

        aesthetic_print(tree, 0)

    except ExecutionCompendiumNotFound:
        aesthetic_print(
            rich.markdown.Markdown("The defined Execution Compendium was not founded!")
        )

    except:
        aesthetic_traceback(show_locals=True)


@compendium.command(name="files-download")
@click.option(
    "--compendium-pid",
    required=False,
    type=str,
    help="Storm WS Compendium identifier (Draft or Record).",
)
@click.option(
    "--draft",
    required=False,
    default=False,
    is_flag=True,
    type=bool,
    help="Flag indicating if the Compendium from where the files will be downloaded is a Draft.",
)
@click.option(
    "-f",
    "--file-key",
    required=False,
    multiple=True,
    help="File key that will be downloaded (Can be multiple values).",
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
    help="Download Output directory.",
)
@click.pass_obj
def compendium_download_files(
    obj,
    compendium_pid=None,
    draft=None,
    file_key=None,
    output_dir=None,
):
    """Download files from a Storm WS Compendium (Draft or Record)."""
    workbench = obj["workbench"]

    try:
        output_dir = workbench.stage.ws.compendium.download_files(
            compendium_pid, draft, output_dir, file_key or "all"
        )

        tree = aesthetic_tree_base(
            title="\n[bold]Compenium Files - Download[/bold]",
            children=[
                f"[blue]Download Path[/blue]: {output_dir}",
                f"[blue]Status[/blue]: [green]Downloaded[/green]",
            ],
        )

        aesthetic_print(tree, 0)

    except ExecutionCompendiumNotFound:
        aesthetic_print(
            rich.markdown.Markdown("The defined Execution Compendium was not founded!")
        )

    except ValueError:
        aesthetic_print(
            rich.markdown.Markdown(
                "Before downloading the files, you need to define a "
                "`--execution-compendium-name` or `--draft-pid`"
            )
        )

    except NotADirectoryError:
        aesthetic_print(
            rich.markdown.Markdown(
                "The `-o/-output-dir` parameter should be a directory."
            )
        )

    except:
        aesthetic_traceback(show_locals=True)


@compendium.command(name="files-list")
@click.option(
    "--id",
    required=True,
    type=str,
    help="Compendium identifier.",
)
@click.option(
    "--draft",
    required=False,
    default=False,
    is_flag=True,
    type=bool,
    help="Flag indicating if the Compendium selected is a Draft.",
)
@click.pass_obj
def compendium_list_files(obj, id, draft):
    """List Compendium files."""
    workbench = obj["workbench"]

    try:
        compendium_files = workbench.stage.ws.compendium.list_files(id, draft)

        if compendium_files:
            # declaring the table structure:
            table_declaration = {
                "Name": "key",
                "Mimetype": "mimetype",
                "Checksum (MD5)": "checksum",
                "Version ID": "version_id",
            }

            # generating and presenting the table.
            table = aesthetic_table_by_document(
                "Search result - Compendium Files", table_declaration, compendium_files
            )
            aesthetic_print(table, 0)

        else:
            aesthetic_print("Empty search result!", 0)
    except:
        aesthetic_traceback(show_locals=True)

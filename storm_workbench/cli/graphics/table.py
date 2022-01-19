# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import List, Tuple, Dict

from pydash import py_
from rich.table import Table
from storm_core.index.graph import VertexStatus

from storm_workbench import constants
from storm_workbench.cli.graphics.aesthetic import aesthetic_print


def aesthetic_table_base(title: str, columns: List[str], rows: List[Tuple]) -> Table:
    """Create a simple `rich.table.Table`.

    Args:
        title (str): Table title.

        columns (List[str]): Table columns.

        rows (List[Tuple]): Table rows (tuples with same length of columns.

    Returns:
        Table: Created table.
    """
    table = Table(
        show_header=True, header_style="bold", title_justify="center", title=title
    )

    # adding columns
    [table.add_column(column, justify="center") for column in columns]

    # adding rows
    [table.add_row(*row) for row in rows]

    return table


def aesthetic_table_by_document(
    title: str, table_declaration: Dict, documents: List[object]
):
    """Aesthetic table by document declaration.

    This function allow the creation of Aesthetic tables using a generic and easy-to-use
    declaration. This declaration must be a dictionary with the following structure:

        {
            "<table column name>": "path.to.property"
        }

    The dictionary keys is used as the table columns. Each key value define a path to the property
    that should be extracted from the documents to be used as row values.

    Args:
        title (str): Table title

        table_declaration (Dict): Dict with the table declaration.

        documents (List[object]): List with the objects used to populate the table.

    Returns:
        Table: Created table.

    Note:
        This function uses the `pydash.get` function for the attribute extraction.
        For more information about it, please, check the official pydash documentation:
        <https://pydash.readthedocs.io/en/latest/api.html#pydash.objects.get>.
    """
    # defining the table columns
    table_columns = list(table_declaration.keys())

    # creating the rows
    attribute_definitions = table_declaration.values()

    # extracting attributes from the documents
    table_rows = (
        py_.chain(documents)
        .map(
            lambda x: (
                py_.map(
                    attribute_definitions, lambda definition: py_.to_string(py_.get(x, definition))
                )
            )
        )
        .value()
    )

    return aesthetic_table_base(title=title, columns=table_columns, rows=table_rows)


def aesthetic_table_index_ls(execution_compendia):
    """Show the execution compendia in a high-level table.

    Args:
        execution_compendia (List[ExecutionCompendiumModel]): List of Execution Compendium Model object.

    Returns:
        None: The table will be printed in the terminal.
    """
    # defining icons for each status (the current available status is: `updated` and `outdated`)
    status_emoji = {
        VertexStatus.Updated: ":heavy_check_mark:",
        VertexStatus.Outdated: ":cross_mark:",
    }

    # defining row style
    row_template = "[bold {color}]{status}[/bold {color}]{emoji}"

    # creating the table with the following columns:
    # uuid | pid | name | description | command | status
    columns = ["Name", "Description", "Command", "PID (in the service)", "Status"]

    # preparing the table rows
    rows_formated = []

    for row in execution_compendia:
        # defining status style based on value
        row_status = row.status
        row_emoji = status_emoji[row_status]
        row_status_color = constants.GRAPH_DEFAULT_VERTICES_COLOR[row_status]

        rows_formated.append(
            (
                row.name,
                row.description or "-",
                row.command,
                row.pid or "-",
                row_template.format(
                    color=row_status_color, status=row_status, emoji=row_emoji
                ),
            )
        )

    table = aesthetic_table_base(
        title="[bold]Execution Compendia Index[/bold]",
        columns=columns,
        rows=rows_formated,
    )

    aesthetic_print(table, 0)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import List, Tuple

from rich.table import Table
from storm_core.index.graph import VertexStatus

from storm_workbench.constants import GraphStyleConfig
from storm_workbench.cli.graphics.aesthetic import aesthetic_print


def table_simple(title: str, columns: List[str], rows: List[Tuple]) -> Table:
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


def show_table_execution_index_status(graph_df: "pandas.core.frame.DataFrame"):
    """Print a graph as a table.

    Args:

        graph_df (pandas.core.frame.DataFrame): Graph vertices that will be printed.

    Returns:
        None: The table will be printed on the terminal.
    """
    # defining icons for each status (the current available status is: `updated` and `outdated`)
    emojis = {
        VertexStatus.Updated: ":heavy_check_mark:",
        VertexStatus.Outdated: ":cross_mark:",
    }

    # defining row style
    row_template = "[bold {color}]{status}[/bold {color}]{emoji}"

    # preparing table columns
    columns = ["Execution ID", "Command", "Status"]

    # preparing table rows
    rows = []

    for _, row in graph_df.iterrows():
        # defining status style based on value
        row_status = row.status
        row_emoji = emojis[row_status]
        row_status_color = GraphStyleConfig.GRAPH_DEFAULT_VERTICES_COLOR[row_status]

        rows.append(
            (
                row["name"],
                row.command,
                row_template.format(
                    color=row_status_color, status=row_status, emoji=row_emoji
                ),
            )
        )

    table = table_simple(
        title="[bold]Execution status[/bold]",
        columns=columns,
        rows=rows,
    )

    aesthetic_print(table, 0)

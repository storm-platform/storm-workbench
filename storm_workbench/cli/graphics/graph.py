# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import List, Tuple, Union

from igraph import Graph

try:
    from asciidag.graph import Graph as AsciiGraph
    from asciidag.node import Node
except ImportError:
    raise ModuleNotFoundError(
        "To use the Graph visualization module, please, install the asciidag library: "
        "`pip install asciidag` or `poetry add asciidag`"
    )


def _ascii_dag(graph: Graph) -> Union[None, "AsciiGraph"]:
    """Generate a ASCII Directed Acyclic Graph (DAG).

    Args:
        graph (igraph.Graph): Graph instance that is used to generate the ASCII DAG.

    Returns:
        Union[None, AsciiGraph]: If the graph is displayed, the created graph
        instance is returned. Otherwise, None will be returned.
    """

    def vertex_parents(vertex_id: int, edgelist: List[Tuple]) -> List[Tuple]:
        """Return all vertex parents based on a edge list.

        Args:
            vertex_id (int): Vertex ID.

            edgelist (List[Tuple]): List with tuples with all graph edges.

        Returns:
            List[Tuple]: Edges that is related to `vertex_id`.
        """
        return list(filter(lambda x: x[0] == vertex_id, edgelist))

    if not graph:
        return None  # initially, the project does not have a graph.
    ascii_graph = AsciiGraph()

    # generate ascii nodes
    edgelist = graph.get_edgelist()

    nodes = {
        v.index: Node(
            f"({v['command']})"
            if "command" in v.attributes()
            else v["name"]
        )
        for v in graph.vs
    }

    # connect the nodes
    for vertex in graph.vs:
        node_parents = vertex_parents(vertex.index, edgelist)

        nodes[vertex.index].parents.extend([nodes[i[1]] for i in node_parents])

    # show!
    ascii_graph.show_nodes(list(nodes.values()))
    return ascii_graph


def show_ascii_graph(graph: Graph):
    """Display the Executions DAG on the terminal.

    Args:
        graph (Graph): Graph Index object.

    Returns:
        None: Graph will be presented on the CLI terminal.
    """
    _graph = _ascii_dag(graph)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from typing import List

from rich.tree import Tree


def aesthetic_tree_base(title: str, children: List[str]) -> Tree:
    """Create a simple `rich.tree.Tree`.

    Args:
        title (str): Tree title.

        children (List[str]): List of tree child.

    Returns:
        Tree: Tree object.
    """

    tree = Tree(title)

    for child in children:
        tree.add(child)

    return tree

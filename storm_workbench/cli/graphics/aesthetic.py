# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from time import sleep
from typing import Any

from rich.console import Console


def aesthetic_print(message: Any, wait_time: int = 1, **kwargs):
    """Create aesthetic prints.

    The function takes objects from the rich library and renders
    them on the terminal with the `rich.console.Console`.

    Args:

        message (Any): Message (with style) that will be presented.

        wait_time (int): Waiting time before unlock the terminal.

        kwargs (dict): rich.console.Console extra parameters.

    Returns:
        None: The messages will show on the terminal.
    """
    console = Console(**kwargs.get("console_options", {}))

    console.print(message, **kwargs.get("print_options", {}))
    sleep(wait_time)


def aesthetic_traceback(**kwargs):
    """Create aesthetic traceback.

    Args:
        kwargs: Arguments to the ``rich.console.Console.print_exception``.

    See:
        For more information about the ``rich.console.Console.print_exception``, please
        go to the official documentation: <https://rich.readthedocs.io/en/latest/traceback.html>
    """
    console = Console()
    console.print_exception(**kwargs)

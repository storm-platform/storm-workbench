# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import base64
import hashlib
import os
import re
from pathlib import Path


def _get_user_cache_dir(app_name: str) -> Path:
    """Get the user-specific application cache directory.

    This function finds the user-specific application
    cache directory. Typically, the user cache directories
    are:
        MacOS:   ~/Library/Caches/<AppName>
        Unix:    ~/.cache/<AppName> (XDG default)
        Windows: C:\\Users\\<username>\\AppData\\Local\<AppName>\\Cache

    Args:
        app_name (str): Application name.

    Returns:
        Path: Path to the application cache directory.

    Note:
        This function was adapted from the ``python-poetry`` source code. Currently, we only support the Linux
        implementation.

    See:
        See the original implementation of this function in the ``python-poetry``
        repository: <https://github.com/python-poetry/poetry/blob/f6022eade7485a3b017ef0c8060dffed12e3cdb2/src/poetry/utils/appdirs.py#L32>
    """
    return Path(
        os.path.join(
            os.getenv("XDG_DATA_HOME", os.path.expanduser("~/.local/share")), app_name
        )
    )


def _generate_storage_name(name: str, cwd: str) -> str:
    """Generate a name for the reproducible storage.

    Args:
        name (str): Name used as base to create the reproducible storage name.

        cwd (str): Current working directory.

    Returns:
        str: Reproducible storage name.

    Note:
        This function was adapted from ``python-poetry`` source code.

    See:
        See the original implementation of this function in the ``python-poetry``
        repository: <https://github.com/python-poetry/poetry/blob/f6022eade7485a3b017ef0c8060dffed12e3cdb2/src/poetry/utils/env.py#L1060>
    """
    name = name.lower()
    sanitized_name = re.sub(r'[ $`!*@"\\\r\n\t]', "_", name)[:42]
    normalized_cwd = os.path.normcase(cwd)
    h = hashlib.sha256(normalized_cwd.encode()).digest()
    h = base64.urlsafe_b64encode(h).decode()[:8]

    return f"{sanitized_name}-{h}"


def create_reproducible_storage(name: str, cwd: Path) -> Path:
    """Create a directory to store the Storm Workbench files.

    Args:
        name (str): Name used as base to create the reproducible storage name.

        cwd (str): Current working directory.

    Returns:
        Path: Path to the reproducible storage.
    """
    cache_dir_path = _get_user_cache_dir("storm-workbench")
    storage_name = _generate_storage_name(name, str(cwd))

    storage_path = cache_dir_path / storage_name
    storage_path.mkdir(parents=True, exist_ok=True)

    return storage_path

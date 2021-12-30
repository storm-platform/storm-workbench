# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import importlib
from pathlib import Path
from typing import Type

from dynaconf import Dynaconf

from storm_core import ReproducibleSession
from storm_core.execution import (
    ExecutionEngine,
    ExecutionEngineFilesConfig,
    ExecutionEngineServicesConfig,
)

from storm_core.index.graph import GraphManager
from storm_core.helper.persistence import PicklePersistenceContainer

from storm_workbench.constants import WorkbenchDefinitions
from storm_workbench.location import create_reproducible_storage


def _import_class(class_path: str) -> Type:
    """Load a class from a string path definition.

    Args:
        class_path (str): String with the complete module-path to the class
        to be imported. The class must be declared as follow in the string:

            path.to.class.module:ClassName
    Returns:
        Type: The class imported.
    """
    class_path, class_name = class_path.split(":")

    module = importlib.import_module(class_path)

    return getattr(module, class_name)


def find_workbench_definition_file(cwd: Path = None) -> Path:
    """Find for a workbench definition file.

    This function finds a workbench definition file in the ``cwd`` directory
    and their parents.

    Args:
        cwd (Path): Base directory where the search will be start.

    Returns:
        Path: Path to the founded workbench definition file.

    Raises:
        RuntimeError: When the workbench definition file is not found.

    Note:
        This function was adapted from the ``python-poetry`` source code. Currently, we only support the Linux
        implementation.

    See:
        See the original implementation of this function in the ``python-poetry``
        repository: <https://github.com/python-poetry/poetry-core/blob/af08f1ce720da467c9bf3d43eed3d9ebaf4ad7fb/src/poetry/core/factory.py#L438>
    """
    cwd = Path(cwd or Path.cwd())
    candidates = [cwd]
    candidates.extend(cwd.parents)

    for path in candidates:
        workbench_file = path / WorkbenchDefinitions.WB_DEFINITION_FILE

        if workbench_file.exists():
            return workbench_file

    else:
        raise RuntimeError("Workbench not found!")


def load_workbench_configuration(cwd: Path = None) -> Dynaconf:
    """Load the workbench configuration files.

    This function loads the workbench definition file and the user's secrets file.

    Args:
        cwd (Path): Base directory to find the workbench definition files.

    Returns:
        Dynaconf: Configuration object.

    Raises:
        RuntimeError: When the workbench definition file is not found.
    """
    # loading the workbench definition file
    workbench_definition_file = find_workbench_definition_file(cwd)

    # loading configurations
    workbench_configuration = Dynaconf(settings_files=[workbench_definition_file])
    workbench_configuration.tool.storm.basepath = workbench_definition_file.parent

    return workbench_configuration


def create_reproducible_session(
    workbench_configuration: Dynaconf,
) -> ReproducibleSession:
    """Create a reproducible session for the current workbench.

    Args:
        workbench_configuration (Dynaconf): Workbench configuration object.

    Returns:
        ReproducibleSession: Reproducible Session object.
    """
    reproducible_storage = create_reproducible_storage(
        workbench_configuration.tool.storm.name,
        workbench_configuration.tool.storm.basepath,
    )

    # configuring the session executor
    executor_class = _import_class(
        WorkbenchDefinitions.WB_AVAILABLE_EXECUTORS.get(
            workbench_configuration.tool.storm.executor.get(
                "type", WorkbenchDefinitions.WB_DEFAULT_EXECUTOR
            )
        )
    )
    executor_obj = executor_class(
        **workbench_configuration.tool.storm.executor.get("options") or {}
    )

    # Execution engine configuration objects
    engine_configuration = ExecutionEngineServicesConfig(executor_obj)
    engine_files = ExecutionEngineFilesConfig(
        storage_dir=reproducible_storage / "executions",
        working_directory=workbench_configuration.tool.storm.basepath,
        data_objects=workbench_configuration.tool.storm.get("data_objects"),
        ignored_data_objects=workbench_configuration.tool.storm.get(
            "ignored_data_objects"
        ),
        files_checksum_algorithm=workbench_configuration.tool.storm.get(
            "files_checksum_algorithm", "md5"
        ),
        ignored_environment_variables=workbench_configuration.tool.storm.get(
            "ignored_environment_variables"
        ),
    )

    # Creating the execution engine.
    engine = ExecutionEngine(engine_configuration, engine_files)

    # Graph manager
    graph_index = None
    meta = reproducible_storage / "meta"

    if meta.exists():
        graph_index = PicklePersistenceContainer.load(reproducible_storage / "meta")

    graph_manager = GraphManager(graph_index)

    workbench_configuration.tool.storm.storage = reproducible_storage
    return ReproducibleSession(engine, graph_manager)

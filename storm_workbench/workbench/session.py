# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

from pydash import py_
from storm_core import ReproducibleSession
from storm_core.execution import (
    ExecutionEngine,
    ExecutionEngineFilesConfig,
    ExecutionEngineServicesConfig,
)
from storm_core.helper.persistence import PicklePersistenceContainer
from storm_core.index.graph import GraphManager

from storm_workbench import constants
from storm_workbench.entry_point import load_entry_point
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


def create_reproducible_session(
    reproducible_storage: Path,
    workbench_definition: WorkbenchDefinitionFile,
) -> ReproducibleSession:
    """Create a reproducible session for the current workbench.

    Args:
        reproducible_storage (Path): Directory where the Workbench session files (e.g., Configuration
        file, database file and so on) are stored.

        workbench_definition (WorkbenchDefinitionFile): Workbench configuration object.

    Returns:
        ReproducibleSession: Reproducible Session object.
    """
    # configuring the session executor
    executor_cls_name = workbench_definition.definitions.tool.storm.executor.get(
        "type", constants.WB_DEFAULT_EXECUTOR
    )

    # getting the available Storm Core Executor classes
    # from the entry point.
    executor_classes = load_entry_point(constants.CORE_EXECUTOR_ENTRYPOINT)

    # filtering by the user defined executor class name.
    executor_cls = (
        py_.chain(executor_classes)
        .filter(lambda x: x.name == executor_cls_name)
        .head()
        .value()
    )

    executor_obj = executor_cls(
        **workbench_definition.definitions.tool.storm.executor.get("options") or {}
    )

    # Execution engine configuration objects
    engine_configuration = ExecutionEngineServicesConfig(executor_obj)
    engine_files = ExecutionEngineFilesConfig(
        storage_dir=reproducible_storage / "compendia",
        working_directory=workbench_definition.definitions.tool.storm.basepath,
        data_objects=workbench_definition.definitions.tool.storm.get("data_objects"),
        ignored_data_objects=workbench_definition.definitions.tool.storm.get(
            "ignored_data_objects"
        ),
        files_checksum_algorithm=workbench_definition.definitions.tool.storm.get(
            "files_checksum_algorithm", "md5"
        ),
        ignored_environment_variables=workbench_definition.definitions.tool.storm.get(
            "ignored_environment_variables"
        ),
    )

    # Creating the execution engine.
    engine = ExecutionEngine(engine_configuration, engine_files)

    # Graph manager
    graph_index = None

    meta_dir = reproducible_storage / "workflow"
    meta_dir.mkdir(exist_ok=True, parents=True)

    meta = meta_dir / "meta"

    if meta.exists():
        graph_index = PicklePersistenceContainer.load(meta)

    graph_manager = GraphManager(graph_index)
    return ReproducibleSession(engine, graph_manager)

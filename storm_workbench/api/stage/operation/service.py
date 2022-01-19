# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json
from pathlib import Path
from typing import Union, List

from storm_core.parser import ShellCommandParser, load_stormfile

from storm_workbench.api.backstage.database.model import ExecutionCompendiumModel
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.api.stage.decorator import pass_database_service
from storm_workbench.exceptions import InvalidCommand


class ExecutionOperationService(BaseStageService):
    """Execution operation service class.

    This class provides methods to execute scripts
    in a reproducible way.
    """

    @pass_database_service
    def __init__(self, config, backstage, database_service):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration file.

            backstage: (BackstageAccessor): Accessor to low-level operations API.

            database_service (DatabaseService): Database service object.
        """
        super(ExecutionOperationService, self).__init__(config, backstage)

        self._database_service = database_service

    def run(
        self, name: str = None, description=None, command=None, stormfile=None
    ) -> List[ExecutionCompendiumModel]:
        """Execute a command and save it in an Execution Compendium.

        This method execute a command and create an ``Execution Compendium`` with
        all materials used by the command during execution. In these materials
        are included the ``software packages``, ``data``, ``scripts`` and the
        ``execution provenance``.

        Args:
            name (str): Name of the execution.

            description (str): Basic description of the execution.

            command (str): Command to be executed.

            stormfile (Union[str, Path]): Stormfile with the description of an execution pipeline.

        Returns:
            List[ExecutionCompendiumModel]: List of the created/updated execution compendium.
        """
        if command:
            execution_plan = ShellCommandParser.parse(list(command))

        elif stormfile:
            execution_plan = load_stormfile(stormfile)

        else:
            raise InvalidCommand(
                "To run a reproducible command you need to define a ``command`` or specify "
                "a Stormfile (``--stormfile``)."
            )

        # running the execution plan!
        executed_compendia = self._backstage.execution.op.run(execution_plan)

        # saving (or updating) the generated compendia.
        result_compendia = []

        for executed_compendium in executed_compendia:
            # base object
            compendium_object = ExecutionCompendiumModel(
                name=name,
                description=description,
                uuid=executed_compendium.name,
                command=str(executed_compendium.command),
            )

            # saving in the database.
            record_compendium = self._database_service.upsert_record(compendium_object)
            result_compendia.append(record_compendium)

        # saving the session modifications.
        self._backstage.session.save()

        return result_compendia

    def update(self):
        """Update the ``outdated`` Execution Compendia.

        This method re-executes all compendia with the ``outdated`` status. An Execution
        Compendium is marked as ``outdated`` when any of its predecessors have been executed
        after its creation or last execution.
        """
        # search the outdated compendia and re-execute them!
        self._backstage.execution.op.update()

        # saving the session modifications.
        self._backstage.session.save()


class ReExecutionOperationService(BaseStageService):
    """ReExecution operation service class.

    This class provides methods to reproduce previous generated
    experiments.

    The usage of this class methods assumes that the current working
    directory is a valid Workbench with the following structure:

        - <current working directory>
         - compendia (Directory with the compendia environment files);
         - pipeline (Directory with the complete workbench pipeline description);
         - workbench.toml (Workbench description file).

    To create a file hierarchy as the described below, you can use the methods provided
    by the `storm_workbench.api.stage.exporter.compendium.service.CompendiumExporterService` class.
    """

    def run(
        self,
        required_dataset_descriptor_file: Union[str, Path] = None,
        required_environment_variables: List[str] = None,
    ) -> Path:
        """Reproduce a previous generated experiment.

        Args:
            required_dataset_descriptor_file (Union[str, Path]): File with the complete description of the
            files that should be used as input in the reproduction.

            required_environment_variables (List[str]): List with the required environment variables to reexecute the
            experiment.

        Returns:
            Path: Path to the directory where the results will be saved.

        Note:
            1. For more details about the ``required_dataset_descriptor_file`` file format, please, check the
            Storm Core documentation <https://github.com/storm-platform/storm-core/blob/c51d90a3e8132734d8fb5a9efa89d5e96f6bf806/storm_core/execution/engine.py#L168>.

            2. The ``required_environment_variables`` must be a list with string in the following format:

                required_environment_variables = ["environment-variable-name=variable-value"]
        """
        # temporary: import workbench here to avoid
        # circular import error.
        from storm_workbench import Workbench

        # base validations
        dataset_descriptor = {}

        required_environment_variables = required_environment_variables or []
        required_dataset_descriptor_file = required_dataset_descriptor_file or ""

        # checking for input data
        if required_dataset_descriptor_file:
            required_dataset_descriptor_file = Path(required_dataset_descriptor_file)

            if (
                required_dataset_descriptor_file.exists()
                and not required_dataset_descriptor_file.is_file()
            ):
                raise ValueError("The dataset descriptor file must be a valid file!")

            with required_dataset_descriptor_file.open("r") as ifile:
                dataset_descriptor = json.load(ifile)

        # using the current directory as the workbench reproducible storage.
        reproducible_storage_dir = Path.cwd()

        wb = Workbench(
            cwd=reproducible_storage_dir, reproducible_storage=reproducible_storage_dir
        )

        # checking if the index is populated
        if wb.backstage.execution.index.graph_manager.is_empty:
            raise RuntimeError("Execution Compendia Index is empty! Nothing to do.")

        # preparing the results directory
        output_directory_results = reproducible_storage_dir / "reproduction-results"
        output_directory_results.mkdir(exist_ok=True, parents=True)

        # creating the reproduction workbench and run!
        wb.backstage.execution.op.rerun(
            reproducible_storage=output_directory_results,
            required_data_objects=dataset_descriptor,
            required_environment_variables=required_environment_variables,
        )

        return output_directory_results

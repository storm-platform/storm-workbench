# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
import shutil
import tempfile
from pathlib import Path
from typing import Union, List, Tuple

from pydash import py_
from storm_core.helper.persistence import PicklePersistenceContainer
from storm_hasher import StormHasher

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.backstage.database.model import ExecutionCompendiumModel
from storm_workbench.api.stage.exporter.bagit import BagItExporter
from storm_workbench.api.stage.exporter.base import BaseExporter, BaseExporterService
from storm_workbench.template import write_template, markdown_to_html
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class CompendiumExporterService(BaseExporterService):
    """Compendium Exporter Service class.

    This class provides methods to organize and export the
    Workbench's Compendia in a sharable and executable way.

    By default, the exporter used creates a ``BagIt`` compressed
    file with all elements required to reproduce the executions.
    """

    exporter_cls = BagItExporter
    """Exporter class."""

    def __init__(
        self,
        config: WorkbenchDefinitionFile = None,
        backstage: BackstageAccessor = None,
        exporter: BaseExporter = None,
    ):
        super(CompendiumExporterService, self).__init__(config, backstage)

        self._exporter = exporter or self.exporter_cls()

    def save(
        self,
        compendia: List[Tuple[ExecutionCompendiumModel, str]],
        output_dir: Union[str, Path],
        temp_dir: Union[str, Path] = None,
        filename: str = None,
        **kwargs,
    ) -> Path:
        # defining the base information
        package_name = f"{self._config.definitions.tool.storm.name}.zip"

        # defining the directories and validate them.
        output_dir = Path(output_dir)
        temp_dir = Path(temp_dir) if temp_dir else Path(tempfile.mkdtemp())

        for _dir, _name in [(temp_dir, "temp_dir"), (output_dir, "output_dir")]:
            if _dir.exists() and not _dir.is_dir():
                raise ValueError(f"`{_name}` must be a directory.")

            _dir.mkdir(exist_ok=True, parents=True)

        # checking if the index has outdated/empty execution compendia.
        if self._backstage.execution.index.graph_manager.is_empty:
            raise RuntimeError(
                "Export error! You don't have Execution Compendia to export."
            )

        if self._backstage.execution.index.graph_manager.is_outdated:
            raise RuntimeError(
                "Export error! You have some ``outdated`` Execution Compendia. Please, update them to export."
            )

        # compendia directory
        # the created directory will have the following structure:
        #  - compendia/
        #   - *.rpz
        #  - pipeline/
        #   - meta
        #  - package.(md, html)
        #  - workbench.toml
        output_path_compendium = temp_dir / "compendia"
        output_path_compendium.mkdir(exist_ok=True, parents=True)

        # organizing the compendium bundles.
        compendium_exported_bundles = {}

        for compendium, _ in compendia:
            compendium_package = compendium.compendium_package
            compendium_output_file = output_path_compendium / f"{compendium.name}.rpz"

            # validating the checksum
            file_hash = StormHasher(compendium_package["algorithm"]).hash_file(
                compendium_package["key"]
            )
            if file_hash != compendium_package["checksum"]:
                raise RuntimeError(f"Invalid checksum for {compendium_package['key']}")

            shutil.copy(compendium_package["key"], compendium_output_file)
            compendium_exported_bundles[compendium.name] = compendium_output_file

        # pipeline directory
        output_path_pipeline = temp_dir / "pipeline"
        output_path_pipeline.mkdir(exist_ok=True, parents=True)

        # organizing the pipeline object
        pipeline_graph = self._backstage.execution.index.graph_manager.graph

        for compendium_vtx in pipeline_graph.vs:
            # the environment package will be relative to the package.
            compendium_vtx["environment_package"] = os.path.join(
                "compendia", compendium_exported_bundles[compendium_vtx["name"]].name
            )

        # exporting the pipeline graph metafile
        pipeline_meta_file = output_path_pipeline / "meta"
        PicklePersistenceContainer.save(pipeline_graph, pipeline_meta_file)

        # workbench.toml definition file.
        # we will use the default ``workbench.toml`` to allow the
        # ease reproduction via storm-workbench.
        workbench_definition_file = temp_dir / "workbench.toml"

        write_template(
            workbench_definition_file,
            "workbench.toml",
            mode="reproduction",
            executor="paradag.parallel",
            project_name=self._config.definitions.tool.storm.name,
        )

        # exporting the package.md (with general descriptions about the package)
        package_description = temp_dir / "package.md"

        commands = []
        required_files = []
        required_environment_variables = []

        for compendium_vtx in pipeline_graph.vs:
            command = ExecutionCompendiumModel.get(
                ExecutionCompendiumModel.uuid == compendium_vtx["name"]
            )

            commands.append(
                {
                    "id": str(command.uuid),
                    "name": command.name,
                    "description": command.description or "without description",
                    "command": compendium_vtx["command"],
                }
            )

            required_environment_variables.extend(
                py_.get(
                    compendium_vtx, "metadata.others.unpacked_environment_variables", []
                )
            )

            required_files.extend(
                py_.chain(compendium_vtx)
                .get("metadata.others.unpacked_files.datasources")
                .map(lambda x: Path(x).name)
                .value()
            )

        # writing the base package documentation.
        markdown_template = write_template(
            package_description,
            "form/package.md",
            commands=commands,
            package_name=package_name,
            required_files=required_files,
            required_environment_variables=required_environment_variables,
            project_name=self._config.definitions.tool.storm.name,
        )

        markdown_to_html(markdown_template)

        # defining the output file
        output_file = filename or package_name
        output_file = output_dir / output_file

        if output_file.exists():
            output_file.unlink()

        # exporting!
        output_file = self._exporter.save(temp_dir, output_file)

        if Path(tempfile.gettempdir()) in temp_dir.parents:
            shutil.rmtree(temp_dir)

        return output_file

    def load(
        self, file: Union[str, Path], output_dir: Union[str, Path], **kwargs
    ) -> Path:
        # defining the directories and validate them.
        file = Path(file)
        output_dir = Path(output_dir)

        if file.exists() and not file.is_file():
            raise ValueError(f"`{file}` must be a valid file!")

        if output_dir.exists() and not output_dir.is_dir():
            raise ValueError(f"`{file}` must be a valid directory!")

        # importing
        imported_file = self._exporter.load(
            file,
            output_dir,
            jobs=self._config.definitions.tool.storm.exporter.jobs
            if self._config
            else 2,  # nqa
        )

        return imported_file

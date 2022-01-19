# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List, Tuple

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.backstage.database.model import ExecutionCompendiumModel
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class BaseExporter(ABC):
    """Base exporter class.

    An exporter is an entity responsible for organizing and generating
    sharable unity with the dataset/compendium created/used in the
    workbench context.
    """

    @abstractmethod
    def save(self, input_dir: Path, output_file: Path, **kwargs) -> Path:
        """Organize and export the workbench compendium in a sharable (and centralized) package.

        This method receives a directory and transforms it in a unique sharable package
        (like a zip or tar.gz file).
        Args:
            input_dir (Path): Directory that will be saved in the sharable package.

            output_file (Path): File (.zip) where the content will be saved.

            kwargs: Extra parameters to the exporter.
        Returns:
            Path: Path to the generated file.

        Note:
            This kind of exporter assumes that the ``input_dir`` is organized in the final
            organization structure. So, no changes are made in this directory.
        """
        pass

    @abstractmethod
    def load(self, file: Path, output_dir: Path, **kwargs) -> Path:
        """Load an exported compendium package.

        This method loads an already exported workbench compendium.
        Args:
            file (Path): File to be loaded.

            output_dir (Path): Directory where the imported content will be saved.

            kwargs: Extra parameters to the exporter.

        Returns:
            Path: Path to the directory where the content was saved.
        """
        pass


class BaseExporterService(BaseStageService):
    """Service to manage and handle export tasks.

    An Exporter Service is responsible to organize the
    files (Compendia and Dataset) and send them to the
    exporter.
    """

    exporter_cls = BaseExporter
    """Exporter class."""

    def __init__(
        self,
        config: WorkbenchDefinitionFile = None,
        backstage: BackstageAccessor = None,
        exporter: BaseExporter = None,
    ):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration.

            backstage (BackstageAccessor): Accessor object to manipulate the Backstage API (Workbench low-level API).

            exporter (BaseExporter): Exporter object.
        """
        super(BaseExporterService, self).__init__(config, backstage)

        self._exporter = exporter

    def save(
        self,
        compendia: List[Tuple[ExecutionCompendiumModel, str]],
        output_dir: Union[str, Path],
        temp_dir: Union[str, Path] = None,
        filename: str = None,
        **kwargs
    ) -> Path:
        """Export a Workbench content to a sharable unity.

        Args:
            compendia (List[Tuple[ExecutionCompendiumModel, str]]): List of tuple with the Compendium Model
            object and its status.

            output_dir (Union[str, Path]): Directory where the content will be exported.

            temp_dir (Union[str, Path]): Exchange directory to read/write files during the exportation process.

            filename (str): Output filename.

            kwargs: Extra parameters to the Exporter class.

        Returns:
            Path: Path where the output file was saved.

        Note:
            If the ``filename`` was not specified, the output file will be named with the Workbench name.
        """
        pass

    def load(
        self, file: Union[str, Path], output_dir: Union[str, Path], **kwargs
    ) -> Path:
        """Load a unity exported from the Workbench.

        Args:
            file (Union[str, Path]): File to be imported

            output_dir (Union[str, Path]): Directory where the content will extracted.

            kwargs: Extra parameters to the Exporter class.

        Returns:
            Path: Path where the output file was saved.
        """
        pass

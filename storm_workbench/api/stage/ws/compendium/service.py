# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
from pathlib import Path
from typing import Dict, Union, List

from pydash import py_
from storm_client.models.compendium import (
    CompendiumDraft,
    CompendiumRecordList,
    CompendiumFiles,
)

from storm_workbench import constants
from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.api.stage.database.service import DatabaseService
from storm_workbench.api.stage.decorator import pass_database_service
from storm_workbench.api.stage.ws.decorator import pass_project_context
from storm_workbench.api.stage.ws.service import BaseContextualizedService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class CompendiumService(BaseContextualizedService):
    """Compendium service class.

    This class provides methods to use and manage the Compendium
    resources from the Storm WS.
    """

    @pass_project_context
    @pass_database_service
    def __init__(
        self,
        config: WorkbenchDefinitionFile = None,
        backstage: BackstageAccessor = None,
        context: BaseStageService = None,
        database_service: DatabaseService = None,
    ):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration.

            backstage (BackstageAccessor): Accessor object to manipulate the Backstage API (Workbench low-level API).

            context (BaseStageService): Service which defines the context.

            database_service (DatabaseService): Database service object.
        """
        super(CompendiumService, self).__init__(config, backstage, context)

        self._database_service = database_service

    def describe(self, id_: str, is_draft: bool = False) -> Dict:
        """Describe a Storm WS Compendium.

        Args:
            id_ (str): Compendium Identifier.

            is_draft (bool): Flag indicating if the Compendium to describe is a Draft.

        Returns:
            Dict: Compendium description.
        """
        # based on the compendium type, we use different methods
        # from the context.
        compendium_service = self._context.compendium.record
        if is_draft:
            compendium_service = self._context.compendium.draft

        # getting the description
        compendium_description = compendium_service.get(id_)

        # joining the compendium description with the files'
        # description.
        compendium_description = dict(
            **compendium_description, files=compendium_description.links.files
        )

        return compendium_description

    def search(self, user_records: bool = True, **kwargs) -> CompendiumRecordList:
        """Search for available Compendium (Record and Draft) in the Storm WS.

        Args:
            user_records (bool): Flag indicating if the ``user context`` mode must be used.

            kwargs: Extra arguments to search method.

        Returns:
            CompendiumRecordList: List with founded Compendia.
        """
        return self._context.compendium.search(user_records=user_records, **kwargs)

    def new_draft(self, execution_compendium_name: str):
        """Create a new Storm WS Compendium Draft based on an Execution Compendium.

        Args:
            execution_compendium_name (str): Execution Compendium Name.

        Returns:
            CompendiumDraft: Storm WS Compendium Draft created document.
        """
        # getting the execution compendium (database)
        execution_compendium = self._database_service.query_index(
            name=execution_compendium_name, status="updated"
        )

        # execution compendium (indexed)
        execution_compendium, execution_compendium_indexed = execution_compendium[0]

        # creating the compendium draft model.
        compendium_draft = CompendiumDraft()

        # populating the model
        compendium_draft.title = execution_compendium.name
        compendium_draft.description = execution_compendium.description or "_"

        # defining the Storm Core
        # note: in this alpha version, we only support the Storm Core
        # as an environment descriptor. In the future, we will support
        # multiple descriptors.
        compendium_draft.environment_descriptor = dict(
            name=constants.CORE_DESCRIPTOR_NAME,
            uri=constants.CORE_DESCRIPTOR_URI,
            version=constants.CORE_DESCRIPTION_VERSION,
        )

        # adding the input/output/environment package references
        compendium_draft.environment_metadata = dict(files=dict(key="pack.rpz"))

        compendium_draft.inputs = py_.map(
            execution_compendium_indexed.inputs, lambda x: os.path.basename(x["key"])
        )
        compendium_draft.outputs = py_.map(
            execution_compendium_indexed.outputs, lambda x: os.path.basename(x["key"])
        )

        # creating the draft in the Storm WS.
        compendium_draft = self._context.compendium.draft.create(compendium_draft)

        # saving the draft PID in the database.
        execution_compendium.pid = compendium_draft.id
        self._database_service.upsert_record(execution_compendium)

        return compendium_draft

    def upload_draft_files(self, execution_compendium_name: str):
        """Upload the local Execution Compendium files to a Storm WS Compendium Draft.

        Args:
            execution_compendium_name (str): Execution Compendium Name.

        Returns:
            CompendiumDraft: Storm WS Compendium Draft updated document.
        """
        # getting the execution compendium (database and index)
        execution_compendium = self._database_service.query_index(
            name=execution_compendium_name, status="updated"
        )

        # execution compendium (indexed)
        execution_compendium, execution_compendium_indexed = execution_compendium[0]

        # getting the last draft version from Storm WS
        compendium_draft = self._context.compendium.draft.get(execution_compendium.pid)

        # uploading the files
        # > input and outputs
        compendium_draft = self._context.compendium.files.upload_files(
            compendium_draft,
            {
                os.path.basename(file["key"]): file["key"]
                for file in execution_compendium_indexed.inputs
                + execution_compendium_indexed.outputs
                + [execution_compendium_indexed.compendium_package]
            },
            commit_files=True,
            define_files=True,
        )

        return compendium_draft

    def publish_draft(self, compendium_draft_pid: str):
        """Publish a Storm WS Compendium Draft.

        This method make a Storm WS Compendium Draft available in the Project. The publication can be made
        with the Workbench Execution Compendium Name or the Storm WS Compendium Draft PID.

        Args:
            compendium_draft_pid (str): Storm WS Compendium Draft PID.

        Returns:
            str: Storm WS Compendium Draft ID.
        """
        # getting the last draft version from Storm WS
        compendium_draft = self._context.compendium.draft.get(compendium_draft_pid)

        # publishing!
        compendium_record = self._context.compendium.draft.publish(compendium_draft)

        return compendium_record

    def list_files(
        self, compendium_pid: str, is_draft: bool = False
    ) -> CompendiumFiles:
        """List files from a Storm WS Compendium (Draft or Record).

        Args:
            compendium_pid (str): Storm WS Compendium PID.

            is_draft (bool): Flag indicating if the Compendium to describe is a Draft.

        Returns:
            CompendiumFiles: List of files available in the Compendium.
        """
        # selecting the compendium service
        compendium_service = self._context.compendium.record
        if is_draft:
            compendium_service = self._context.compendium.draft

        # getting the compendium
        compendium = compendium_service.get(compendium_pid)

        return compendium.links.files.entries

    def download_files(
        self,
        compendium_pid,
        is_draft: bool = False,
        output_dir: Union[str, Path] = None,
        files: Union[List[str], str] = "all",
    ) -> Path:
        """Download files from a Storm WS Compendium (Draft or Record).

        This method make a Storm WS Compendium Draft available in the Project. The publication can be made
        with the Workbench Execution Compendium Name or the Storm WS Compendium Draft PID.

        Args:
            compendium_pid (str): Storm WS Compendium PID.

            is_draft (bool): Flag indicating if the Compendium to describe is a Draft.

            output_dir (Union[str, Path]): Directory where the downloaded files will be saved.

            files (List[str]): List with the file keys to download.

        Returns:
            Path: Path to the directory where the files were downloaded.

        Note:
            ``files`` argument can be a list with the file keys to download or a string "all",
            indicating downloading all available files.
        """
        # checking the defined directory
        output_dir = Path(output_dir)

        if output_dir.exists() and not output_dir.is_dir():
            raise NotADirectoryError("The defined output directory is a file")

        output_dir.mkdir(exist_ok=True, parents=True)

        # selecting the compendium service
        compendium_service = self._context.compendium.record
        if is_draft:
            compendium_service = self._context.compendium.draft

        # getting the compendium from the Storm WS
        compendium = compendium_service.get(compendium_pid)

        # defining which files will be downloaded
        if files == "all":
            files = None
        elif files:
            files = [files]

        # downloading the files
        self._context.compendium.files.download_files(compendium, output_dir, files)

        return output_dir

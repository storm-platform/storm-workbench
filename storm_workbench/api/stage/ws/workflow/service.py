# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import List

from storm_client.models.workflow import Workflow

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.api.stage.ws.decorator import pass_project_context
from storm_workbench.api.stage.ws.service import BaseContextualizedService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class WorkflowService(BaseContextualizedService):
    """Workflow service class.

    This class provides methods to use and manage the Pipeline
    resources from the Storm WS.
    """

    @pass_project_context
    def __init__(
        self,
        config: WorkbenchDefinitionFile = None,
        backstage: BackstageAccessor = None,
        context: BaseStageService = None,
    ):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration.

            backstage (BackstageAccessor): Accessor object to manipulate the Backstage API (Workbench low-level API).

            context (BaseStageService): Service which defines the context.
        """
        super(WorkflowService, self).__init__(config, backstage, context)

    def create(self, workflow: Workflow):
        """Create a new Workflow in the Storm WS.

        Args:
            workflow (Workflow): Pipeline object.

        Returns:
            Workflow: Workflow object created in the Storm WS.
        """
        created_workflow = self._context.workflow.create(workflow)

        return created_workflow

    def finish(self, id_: str) -> Workflow:
        """Finish a Storm WS Workflow.

        Args:
            id_ (str): Workflow identifier.

        Returns:
            Workflow: Workflow description.
        """
        return self._context.workflow.finalize(id_)

    def delete(self, id_: str):
        """Delete a Storm WS Workflow.

        Args:
            id_ (str): Workflow identifier.

        Returns:
            None: The Workflow will be deleted from the Storm WS.
        """
        self._context.workflow.delete(id_)

    def search(self, **kwargs) -> List[Workflow]:
        """Search for available projects in the Storm WS.

        Args:
            kwargs: Extra arguments to search method.

        Returns:
            List[Workflow]: List with founded Workflows.
        """
        return self._context.workflow.search(**kwargs)

    def describe(self, id_: str) -> Workflow:
        """Describe a Storm WS Workflow.

        Args:
            id_ (str): Workflow Identifier.

        Returns:
            Workflow: Workflow Object.
        """
        # getting the description
        return self._context.workflow.get(id_)

    def add_compendium(self, id_: str, compendium_id: str) -> Workflow:
        """Add a Compendium Record (Published) in the Workflow.

        Args:
            id_ (str): Workflow Identifier.

            compendium_id (str): Compendium Record identifier (Published).

        Returns:
            Workflow: Workflow object created in the Storm WS.
        """
        workflow_obj = self._context.workflow.get(id_)

        # adding the compendium to the workflow.
        workflow_obj.compendia.append(compendium_id)

        # syncing the modified workflow with the service.
        self._context.workflow.sync_compendia(workflow_obj)

        return workflow_obj

    def remove_compendium(self, id_: str, compendium_id: str) -> Workflow:
        """Remove a Compendium Record from the Workflow.

        Args:
            id_ (str): Workflow Identifier.

            compendium_id (str): Compendium Record identifier (Published).

        Returns:
            Workflow: Workflow object updated in the Storm WS.
        """
        workflow_obj = self._context.workflow.get(id_)

        # adding the compendium to the workflow.
        workflow_obj.compendia.remove(compendium_id)

        # syncing the modified workflow with the service.
        self._context.workflow.sync_compendia(workflow_obj)

        return workflow_obj

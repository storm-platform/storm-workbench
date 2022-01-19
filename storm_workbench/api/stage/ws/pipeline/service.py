# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from typing import List

from storm_client.models.pipeline import Pipeline

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.api.stage.ws.decorator import pass_project_context
from storm_workbench.api.stage.ws.service import BaseContextualizedService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class PipelineService(BaseContextualizedService):
    """Pipeline service class.

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
        super(PipelineService, self).__init__(config, backstage, context)

    def create(self, pipeline: Pipeline):
        """Create a new Pipeline in the Storm WS.

        Args:
            pipeline (Pipeline): Pipeline object.

        Returns:
            Pipeline: Pipeline object created in the Storm WS.
        """
        created_pipeline = self._context.pipeline.create(pipeline)

        return created_pipeline

    def finish(self, id_: str) -> Pipeline:
        """Finish a Storm WS Pipeline.

        Args:
            id_ (str): Pipeline identifier.

        Returns:
            Pipeline: Pipeline description.
        """
        return self._context.pipeline.finalize(id_)

    def delete(self, id_: str):
        """Delete a Storm WS Pipeline.

        Args:
            id_ (str): Pipeline identifier.

        Returns:
            None: The Pipeline will be deleted from the Storm WS.
        """
        self._context.pipeline.delete(id_)

    def search(self, **kwargs) -> List[Pipeline]:
        """Search for available projects in the Storm WS.

        Args:
            kwargs: Extra arguments to search method.

        Returns:
            List[Pipeline]: List with founded Pipelines.
        """
        return self._context.pipeline.search(**kwargs)

    def describe(self, id_: str) -> Pipeline:
        """Describe a Storm WS Pipeline.

        Args:
            id_ (str): Pipeline Identifier.

        Returns:
            Pipeline: Pipeline Object.
        """
        # getting the description
        return self._context.pipeline.get(id_)

    def add_compendium(self, id_: str, compendium_id: str) -> Pipeline:
        """Add a Compendium Record (Published) in the Pipeline.

        Args:
            id_ (str): Pipeline Identifier.

            compendium_id (str): Compendium Record identifier (Published).

        Returns:
            Pipeline: Pipeline object created in the Storm WS.
        """
        pipeline_obj = self._context.pipeline.get(id_)

        # adding the compendium to the pipeline.
        pipeline_obj.compendia.append(compendium_id)

        # syncing the modified pipeline with the service.
        self._context.pipeline.sync_compendia(pipeline_obj)

        return pipeline_obj

    def remove_compendium(self, id_: str, compendium_id: str) -> Pipeline:
        """Remove a Compendium Record from the Pipeline.

        Args:
            id_ (str): Pipeline Identifier.

            compendium_id (str): Compendium Record identifier (Published).

        Returns:
            Pipeline: Pipeline object updated in the Storm WS.
        """
        pipeline_obj = self._context.pipeline.get(id_)

        # adding the compendium to the pipeline.
        pipeline_obj.compendia.remove(compendium_id)

        # syncing the modified pipeline with the service.
        self._context.pipeline.sync_compendia(pipeline_obj)

        return pipeline_obj

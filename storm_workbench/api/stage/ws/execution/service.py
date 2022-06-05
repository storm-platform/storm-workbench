# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_client.models.execution import ExecutionJob, ExecutionJobList, ExecutionJobServiceList

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.backstage.argparser import parse_arguments_as_dict
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.api.stage.ws.decorator import pass_project_context
from storm_workbench.api.stage.ws.service import BaseContextualizedService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class ExecutionJobService(BaseContextualizedService):
    """ExecutionJob service class.

    This class provides methods to use and manage the Job
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
        super(ExecutionJobService, self).__init__(config, backstage, context)

    def create(self, job: ExecutionJob):
        """Create a new ExecutionJob in the Storm WS.

        Args:
            job (ExecutionJob): ExecutionJob object.

        Returns:
            Job: Job object created in the Storm WS.
        """
        created_job = self._context.job.create(job)

        return created_job

    def update(self, job: ExecutionJob):
        """Update a ExecutionJob in the Storm WS.

        Args:
            job (Job): Job object.

        Returns:
            Job: Job object updated in the Storm WS.
        """
        selected_job = self._context.job.get(job.id)

        # monkey patch to update the properties.
        for attr in ["service", "pipeline_id"]:
            attr_val = getattr(job, attr)

            if attr_val:  # avoiding consistency problems
                setattr(selected_job, attr, attr_val)

        # saving the modifications
        return self._context.job.save(selected_job)

    def delete(self, id_: str):
        """Delete a Job from the Storm WS.

        Args:
            id_ (str): ExecutionJob Identifier.

        Returns:
            None: The ExecutionJob will be deleted from the Storm WS.
        """
        self._context.job.delete(id_)

    def describe(self, id_: str, **kwargs) -> ExecutionJob:
        """Describe a Storm WS Job.

        Args:
            id_ (str): Job Identifier.

            kwargs: Extra parameters to the HTTP request library.

        Returns:
            Job: Job Object.
        """
        # getting the description
        return self._context.job.get(id_, **kwargs)

    @parse_arguments_as_dict(sep=",", argument_key_value_sep="=", inject_key="json")
    def start(self, id_: str, **kwargs) -> ExecutionJob:
        """Start a Storm WS Job.

        Args:
            id_ (str): Job Identifier.

            kwargs: Extra parameters to the HTTP request library.

        Returns:
            Job: Job Object.
        """
        return self._context.job.start_job(id_, request_options=kwargs)

    def services(self, **kwargs) -> ExecutionJobServiceList:
        """List the available services to execute the Storm WS Job.

        Args:
            kwargs: Extra parameters to the HTTP request library.

        Returns:
            JobServiceList: List with available execution execution services.
        """
        return self._context.job.list_services(**kwargs)

    @parse_arguments_as_dict(sep="&", argument_key_value_sep=":")
    def search(self, **kwargs) -> ExecutionJobList:
        """Search for jobs in the Storm WS.

        Args:
            kwargs: Extra arguments to search method.

        Returns:
            JobList: List with the founded Jobs.
        """
        return self._context.job.search(**kwargs)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_workbench.api.stage.base import BaseStageAccessor
from storm_workbench.api.stage.ws.compendium.service import CompendiumService
from storm_workbench.api.stage.ws.context.service import ContextService
from storm_workbench.api.stage.ws.deposit.service import DepositService
from storm_workbench.api.stage.ws.job.service import JobService
from storm_workbench.api.stage.ws.pipeline.service import PipelineService
from storm_workbench.api.stage.ws.project.service import ProjectService
from storm_workbench.api.stage.ws.service import StormWSService


class ResourceServicesAccessor(BaseStageAccessor):
    """Resource service accessor.

    This class provides high-level methods to access services to
    manage and use Storm WS resources (e.g., Projects, Pipelines).
    """

    @property
    def base(self):
        """Base Storm WS service accessor method."""
        return StormWSService(self._config, self._backstage)

    @property
    def context(self):
        """Context management services."""
        return ContextService(self._config, self._backstage)

    @property
    def project(self):
        """Project service accessor method."""
        return ProjectService(self._config, self._backstage)

    @property
    def compendium(self):
        """Compendium service accessor method."""
        return CompendiumService(self._config, self._backstage)

    @property
    def pipeline(self):
        """Pipeline service accessor method."""
        return PipelineService(self._config, self._backstage)

    @property
    def job(self):
        """Job service accessor method."""
        return JobService(self._config, self._backstage)

    @property
    def deposit(self):
        """Deposit service accessor method."""
        return DepositService(self._config, self._backstage)

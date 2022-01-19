# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.stage.base import BaseStageAccessor
from storm_workbench.api.stage.database.service import DatabaseService
from storm_workbench.api.stage.environment.service import EnvironmentService
from storm_workbench.api.stage.exporter.accessor import ExporterServiceAccessor
from storm_workbench.api.stage.operation.accessor import OperationAccessor
from storm_workbench.api.stage.ws.accessor import ResourceServicesAccessor

from storm_workbench.workbench.settings import WorkbenchDefinitionFile
from storm_workbench.workbench.store import pass_config


class StageAccessor(BaseStageAccessor):
    """Stage Accessor class.

    In the Storm-Workbench, the Stage API provides a high-level, ease-to-use
    API to produce and use Reproducible Research. This Accessor make all services
    provided by the Stage API available using a centralization and API unification
    approach.
    """

    @pass_config
    def __init__(self, backstage: BackstageAccessor, config: WorkbenchDefinitionFile):
        super(StageAccessor, self).__init__(config, backstage)

    @property
    def index(self):
        """Stage API Dataset service."""
        return DatabaseService(self._config, self._backstage)

    @property
    def operation(self):
        """Stage API Operations (Execution and ReExecution) Accessor."""
        return OperationAccessor(self._config, self._backstage)

    @property
    def environment(self):
        """Stage API Environment service."""
        return EnvironmentService(self._config, self._backstage)

    @property
    def exporter(self):
        """Stage API Exporter accessor."""
        return ExporterServiceAccessor(self._config, self._backstage)

    @property
    def ws(self):
        """Stage API Storm WS accessor."""
        return ResourceServicesAccessor(self._config, self._backstage)

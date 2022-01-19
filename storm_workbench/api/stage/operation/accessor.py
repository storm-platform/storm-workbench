# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_workbench.api.stage.accessor import BaseStageAccessor
from storm_workbench.api.stage.operation.service import (
    ExecutionOperationService,
    ReExecutionOperationService,
)


class OperationAccessor(BaseStageAccessor):
    """Operation Accessor class.

    This Accessor provides access to the high-level operations for produce and
    reproduce reproducible executions in the Storm Workbench.
    """

    @property
    def execution(self):
        """Stage API Execution service."""
        return ExecutionOperationService(self._config, self._backstage)

    @property
    def reexecution(self):
        """Stage API ReExecution service."""
        return ReExecutionOperationService(self._config, self._backstage)

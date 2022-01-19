# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_workbench.api.accessor import BaseAccessor

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class BaseStageAccessor(BaseAccessor):
    """Base Stage Accessor.

    Base class for the Stage Accessors.
    """

    def __init__(self, config: WorkbenchDefinitionFile, backstage: BackstageAccessor):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration.

            backstage (BackstageAccessor): Accessor object to manipulate the Backstage API (Workbench low-level API).
        """
        super(BaseStageAccessor, self).__init__(config)

        self._backstage = backstage


class BaseStageService:
    """Base Stage API (high-level API) service.

    In the Storm-Workbench, the Stage API provides a high-level, ease-to-use
    API to produce and use Reproducible Research. This class is the base abstraction
    of the services provided by the Stage API.
    """

    def __init__(
        self,
        config: WorkbenchDefinitionFile = None,
        backstage: BackstageAccessor = None,
    ):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration.

            backstage (BackstageAccessor): Accessor object to manipulate the Backstage API (Workbench low-level API).
        """
        self._config = config
        self._backstage = backstage

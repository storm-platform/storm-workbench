# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class BaseContextualizedService(BaseStageService):
    """Base Contextualized service class.

    A ``Contextualized`` service is a special service which
    is defined inside a context of other service. This class
    provides the base abstraction to create this kind of service.
    """

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
        super(BaseContextualizedService, self).__init__(config, backstage)

        self._context = context


class StormWSService(BaseStageService):
    """General Storm WS service class.

    This class provides methods to manage and access general configurations
    of the Storm WS.
    """

    def authenticate(self):
        """Authenticate user in the Storm WS.

        Returns:
            bool: Flag indicating if the authentication works.
        """
        return self._backstage.ws.client.is_connected

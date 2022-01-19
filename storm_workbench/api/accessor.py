# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_core import ReproducibleSession

from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class BaseAccessor:
    """Base Accessor class."""

    def __init__(self, config: WorkbenchDefinitionFile):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration object.
        """
        self._config = config


class SessionAccessor(BaseAccessor):
    def __init__(self, config: WorkbenchDefinitionFile, session: ReproducibleSession):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration object.

            session (ReproducibleSession): Reproducible Session object.
        """
        super(SessionAccessor, self).__init__(config)

        self._session = session

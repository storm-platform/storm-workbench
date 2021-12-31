# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from dynaconf import Dynaconf
from storm_core import ReproducibleSession
from storm_core.helper.persistence import PicklePersistenceContainer


class SessionAccessor:
    """Session Accessor class."""

    def __init__(self, config: Dynaconf, session: ReproducibleSession):
        """Initializer.

        Args:
            config (Dynaconf): Workbench configuration object.

            session (ReproducibleSession): Reproducible Session object.
        """
        self._config = config
        self._session = session

    @property
    def index(self):
        """Execution index."""
        return self._session.index

    @property
    def op(self):
        """Reproducible Operations."""
        return self._session.op

    def save_session(self):
        """Save the current session object."""
        workbench_storage = self._config.tool.storm.storage
        PicklePersistenceContainer.save(
            self._session.index.graph_manager.graph, workbench_storage / "meta"
        )

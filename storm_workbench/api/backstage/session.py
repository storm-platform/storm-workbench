# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

from storm_core import ReproducibleSession
from storm_core.helper.persistence import PicklePersistenceContainer


class SessionService:
    """Workbench session management.

    Base service to manage the workbench session. Using this class
    is possible to define what modification will be applied in the
    current Workbench.
    """

    def __init__(self, reproducible_storage: Path, session: ReproducibleSession):
        """Initializer.

        Args:
            reproducible_storage (Path): Directory where the Workbench session files (e.g., Configuration
            file, database file and so on) are stored.

            session (ReproducibleSession): Reproducible Session Object.
        """
        self._session = session
        self._reproducible_storage = reproducible_storage

    def save(self):
        """Save the current session."""
        # ToDo: Maybe the "session" can be transformed in a class like the "configuration file".
        PicklePersistenceContainer.save(
            self._session.index.graph_manager.graph,
            self._reproducible_storage / "workflow/meta",
        )

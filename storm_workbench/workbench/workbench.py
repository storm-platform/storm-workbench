# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path
from typing import Union

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.backstage.database import init_database
from storm_workbench.api.stage.accessor import StageAccessor
from storm_workbench.location import create_reproducible_storage
from storm_workbench.workbench.session import create_reproducible_session
from storm_workbench.workbench.settings import WorkbenchDefinitionFile
from storm_workbench.workbench.store import pass_config


class Workbench:
    """Workbench class."""

    @pass_config
    def __init__(
        self,
        cwd: Path = None,
        config: WorkbenchDefinitionFile = None,
        reproducible_storage: Union[str, Path] = None,
    ):
        """Initializer.

        Args:
            cwd (pathlib.Path): Workbench base directory.

            config (WorkbenchDefinitionFile): Workbench configuration object.

            reproducible_storage (Path): Directory where the Workbench session files (e.g., Configuration
            file, database file and so on) are stored.
        """
        self._config = config

        # reproducible storage: where the reproducible
        # files will be stored.
        self._reproducible_storage = (
            reproducible_storage
            or create_reproducible_storage(
                config.definitions.tool.storm.name,
                config.definitions.tool.storm.basepath,
            )
        )

        # session: to manage and access the
        # reproducible operations
        self._reproducible_session = create_reproducible_session(
            self._reproducible_storage, self._config
        )

        # database: to store the relation between the local
        # and online compendia. The database also provides a high-level
        # identifier system to the compendia.
        database_path = self._reproducible_storage / "register"
        database_path.mkdir(exist_ok=True, parents=True)

        init_database(database_path / "register.db")

    @property
    def stage(self):
        """Stage API services accessor."""
        return StageAccessor(self.backstage)

    @property
    def backstage(self):
        """Backstage API services accessor."""
        return BackstageAccessor(self._reproducible_storage, self._reproducible_session)

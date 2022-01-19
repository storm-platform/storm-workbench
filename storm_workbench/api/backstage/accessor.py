# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from copy import deepcopy
from pathlib import Path

from dynaconf import Dynaconf
from pydash import py_
from storm_client import Storm as StormClient
from storm_core import ReproducibleSession

from storm_workbench.api.accessor import BaseAccessor, SessionAccessor
from storm_workbench.api.backstage.session import SessionService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile
from storm_workbench.workbench.store import pass_config


class ExecutionAccessor(SessionAccessor):
    """Execution Accessor class.

    This Accessor provides the base operations to produce and reproduce reproducible
    executions in the Storm Workbench. The current implementation is based on Storm Core.
    Please check the official Storm Core repository for more information about it:
    <https://github.com/storm-platform/storm-core>.
    """

    def __init__(self, config: WorkbenchDefinitionFile, session: ReproducibleSession):
        """Initializer.

        Args:
            config (Dynaconf): Workbench configuration object.

            session (ReproducibleSession): Reproducible Session object.
        """
        super(SessionAccessor, self).__init__(config)

        self._session = session

    @property
    def index(self):
        """Execution index."""
        return self._session.index

    @property
    def op(self):
        """Reproducible Operations."""
        return self._session.op


class WebServiceAccessor(BaseAccessor):
    """Storm Service Accessor class.

    The Storm Workbench can connect and use the Storm WS to produce in a collaborative way,
    reproducible research results. This Accessor provides the access to the Storm WS client.
    Using this client, all Storm WS endpoints can be accessed.

    The current implementation is based on Storm Client. Please check the official Storm Client
    repository for more information about it:: <https://github.com/storm-platform/storm-client>.
    """

    def __init__(self, config: WorkbenchDefinitionFile):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration object.
        """
        super(WebServiceAccessor, self).__init__(config)

    @property
    def client(self):
        """Storm WS service client."""
        service_url = py_.get(self._config.definitions, "tool.storm.ws.url")
        service_access_token = py_.get(self._config.definitions, "access-token")

        return StormClient(
            url=service_url,
            access_token=service_access_token,
            verify=False,
            timeout=None,
        )


class BackstageAccessor(BaseAccessor):
    """Backstage Accessor class.

    In the Storm-Workbench, the Backstage API provides a low-level functionality
    to manage the datasets, executions and packages. This Accessor make all services
    provided by the Backstage API available using a centralization and API unification
    approach.
    """

    @pass_config
    def __init__(
        self,
        reproducible_storage: Path,
        session: ReproducibleSession,
        config: WorkbenchDefinitionFile,
    ):
        """Initializer.

        Args:
            reproducible_storage (Path): Directory where the Workbench session files (e.g., Configuration
            file, database file and so on) are stored.

            config (WorkbenchDefinitionFile): Workbench configuration object.

            session (ReproducibleSession): Reproducible Session object.
        """
        super(BackstageAccessor, self).__init__(config)

        self._session = session
        self._reproducible_storage = reproducible_storage

    @property
    def storage(self):
        """Storage to store the Workbench configuration files."""
        return deepcopy(self._reproducible_storage)  # read-only!

    @property
    def ws(self):
        """Service class for Web Services."""
        return WebServiceAccessor(self._config)

    @property
    def execution(self):
        """Execution management service."""
        return ExecutionAccessor(self._config, self._session)

    @property
    def session(self):
        """Workbench session management service."""
        return SessionService(self._reproducible_storage, self._session)

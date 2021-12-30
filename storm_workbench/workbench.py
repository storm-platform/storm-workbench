# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

from storm_workbench.accessor import SessionAccessor
from storm_workbench.settings import (
    load_workbench_configuration,
    create_reproducible_session,
)


class Workbench:
    def __init__(self, cwd: Path = None):

        self._workbench_config = load_workbench_configuration(cwd)
        self._reproducible_session = create_reproducible_session(self._workbench_config)

    @property
    def config(self):
        return self._workbench_config

    @property
    def session(self):
        return SessionAccessor(self._workbench_config, self._reproducible_session)

    @property
    def service(self):
        return object()  # ToDo: Service class.

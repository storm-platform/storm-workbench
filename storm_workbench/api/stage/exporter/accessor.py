# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_workbench.api.stage.accessor import BaseStageAccessor
from storm_workbench.api.stage.exporter.compendium.service import (
    CompendiumExporterService,
)
from storm_workbench.api.stage.exporter.dataset.service import DatasetExporterService


class ExporterServiceAccessor(BaseStageAccessor):
    """Exporter service accessor.

    This Accessor provides access to the Compendia and
    Dataset exporter services.
    """

    @property
    def compendium(self):
        """Compendium exporter service."""
        return CompendiumExporterService(self._config, self._backstage)

    @property
    def dataset(self):
        """Dataset exporter service."""
        return DatasetExporterService(self._config, self._backstage)

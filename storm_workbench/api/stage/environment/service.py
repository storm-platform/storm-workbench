# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import shutil
from pathlib import Path

from hurry.filesize import size

from storm_workbench.api.stage.base import BaseStageService


class EnvironmentService(BaseStageService):
    """Environment management service.

    This class provides a high-level API to manage the
    workbench environment.
    """

    @property
    def path(self) -> Path:
        """Environment directory."""
        return self._backstage.storage

    @property
    def size(self):
        """Environment directory size (bytes).

        Note:
            Method based on: <https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python>
        """
        nbytes = sum(f.stat().st_size for f in self.path.glob("**/*") if f.is_file())
        return size(nbytes)

    def clean(self):
        """Remove all environment data and files."""
        shutil.rmtree(self._backstage.storage)

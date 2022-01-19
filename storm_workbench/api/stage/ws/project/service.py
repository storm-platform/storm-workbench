# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from typing import List

from storm_client.models.project import Project

from storm_workbench.api.stage.base import BaseStageService


class ProjectService(BaseStageService):
    """Storm WS Project service class.

    This class provides high-level methods to access and manage the
    Storm WS projects.
    """

    def describe(self, id_: str) -> Project:
        """Describe a Storm WS project.

        Args:
            id_ (str): Project identifier.

        Returns:
            Project: Project description.
        """
        return self._backstage.ws.client.project.get(id_)

    def create(self, project: Project):
        """Create a new Project in the Storm WS.

        Args:
            project (Project): Project object.

        Returns:
            Project: Project object created in the Storm WS.
        """
        created_project = self._backstage.ws.client.project.create(project)

        return created_project

    def finish(self, id_: str) -> Project:
        """Finish a Storm WS Project.

        Args:
            id_ (str): Project identifier.

        Returns:
            Project: Project description.
        """
        return self._backstage.ws.client.project.finalize(id_)

    def search(self, user_records: bool = True, **kwargs) -> List[Project]:
        """Search for available projects in the Storm WS.

        Args:
            user_records (bool): Flag indicating if the ``user context`` mode must be used.

            kwargs: Extra arguments to search method.

        Returns:
            List[Project]: List with founded Projects.
        """
        return self._backstage.ws.client.project.search(
            user_records=user_records, **kwargs
        )

    def __call__(self, id_):
        """Create a Project context."""
        return self._backstage.ws.client.project(id_)

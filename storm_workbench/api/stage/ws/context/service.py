# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import tomlkit
from pydash import py_

from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.template import write_template


class ContextService(BaseStageService):
    """Context manager service class.

    In the Storm Workbench, the access for some resources of the Storm WS
    is controlled by a context. This class provides the methods to manage
    this context.

    To persist the context configuration we use a toml file. This toml file
    is stored in the base Workbench directory.
    """

    def _context_store(self):
        """Get the available context store file."""
        context_store = self._config.definitions.tool.storm.secrets_file

        if not context_store.exists():
            # creating the context file
            write_template(context_store, "config/secrets.toml")

        return context_store

    def _context_store_obj(self):
        """Get the current store object."""
        context_store = self._context_store()

        with context_store.open(mode="r") as ifile:
            # loading the store file and changing it
            return tomlkit.load(ifile)

    def _activate(self, _id: str, key: str):
        """Base function to apply the context activation in the
        context store.

        This function apply the ``_id`` in the ``key`` on the context object.

        Args:
            _id (str): Entity identifier (in the Storm WS) to use as context.

            key (str): Attribute path (dot notation supported) where the ``_id`` will
            be saved in the context object.

        Returns:
            None: The context modification is done in-place.
        """
        context_store = self._context_store()

        with context_store.open(mode="r") as ifile:
            # loading the store file and changing it
            context_content = tomlkit.load(ifile)

            context_content = py_.set(context_content, key, _id)

            with context_store.open(mode="w") as ofile:
                tomlkit.dump(context_content, ofile)

    @property
    def project(self):
        """Current activated Project."""
        context_obj = self._context_store_obj()

        return str(py_.get(context_obj, "project"))

    def activate_project(self, _id: str):
        """Activate a project in the context.

        Args:
            _id (str): Project identifier (in the Storm WS).

        Returns:
            None: The context will be updated in-place.
        """
        self._activate(_id, "project")

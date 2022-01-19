# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from datetime import datetime

import peewee
import randomname

from storm_workbench.api.backstage.database import db


class BaseModel(peewee.Model):
    """Base peewee model class."""

    created = peewee.DateTimeField(null=True, default=datetime.utcnow)
    """Creation timestamp."""

    updated = peewee.DateTimeField(null=True, default=datetime.utcnow)
    """Last update timestamp"""

    class Meta:
        database = db


class ExecutionCompendiumModel(BaseModel):
    """Execution model class.

    In the context of Storm Workbench, an Execution Compendium is a unity
    responsible for centralize all materials used to produce some research
    results using a script. So, these materials includes the ``software
    packages``, ``data``, ``scripts`` and the ``execution provenance``.
    """

    pid = peewee.CharField(null=True)
    """Persistent identifier (in the Storm WS)."""

    uuid = peewee.UUIDField(primary_key=True)
    """Unique execution compendium identifier."""

    name = peewee.CharField(default=randomname.get_name, null=False, unique=True)
    """Execution name (Optional)."""

    description = peewee.TextField(null=True)
    """Execution description (Optional)."""

    command = peewee.TextField(null=False)
    """Execution command."""

    status = peewee.CharField(null=False)
    """Execution status."""

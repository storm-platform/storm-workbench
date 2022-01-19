# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

import peewee

db = peewee.SqliteDatabase(None)


def init_database(path: Path, **kwargs):
    """Initialize a sqlite database with the workbench models.

    Args:
        path (pathlib.Path): Full path to the sqlite database file.

        kwargs: Extra args to the ``peewee.SqliteDatabase.init`` method.

    See:
        For more details about the ``peewee.SqliteDatabase.init``, please check the
        official documentation: http://docs.peewee-orm.com/en/latest/peewee/database.html#run-time-database-configuration
    """
    # checking if file exists before the init
    is_to_create_tables = False

    if not path.is_file():
        is_to_create_tables = True

    # initializing the database
    db.init(Path("sqlite://") / path, **kwargs)

    if is_to_create_tables:
        # in a near future, if needed, we can use a object factory to
        # avoid circular imports.
        from storm_workbench.api.backstage.database.model import (
            ExecutionCompendiumModel,
        )

        db.create_tables([ExecutionCompendiumModel])

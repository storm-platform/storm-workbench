# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps

from storm_workbench.api.stage.database.service import DatabaseService


def pass_database_service(f):
    """Pass the Database Service.

    This decorator creates a ``Database Service``
    and inject it in the decorated function.
    """

    @wraps(f)
    def wrapper(self, *args, config=None, backstage=None, **kwargs):
        # creating the database service.
        # this is not the more general to do this!
        database_service = DatabaseService(*args)

        # injecting!
        return f(self, *args, database_service=database_service, **kwargs)

    return wrapper

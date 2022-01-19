# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps

from storm_workbench.api.stage.ws.context.service import ContextService
from storm_workbench.api.stage.ws.project.service import ProjectService


def pass_project_context(f):
    """Pass the Project Context Service.

    This decorator creates a ``Project Service``
    and inject it as a context in the decorated function.
    """

    @wraps(f)
    def wrapper(self, *args, config=None, backstage=None, **kwargs):
        # creating the Context Service.
        context_service = ContextService(*args)

        # creating the project based on context service
        project_service = ProjectService(*args)
        project_context = project_service(context_service.project)

        # injecting!
        return f(self, *args, context=project_context, **kwargs)

    return wrapper

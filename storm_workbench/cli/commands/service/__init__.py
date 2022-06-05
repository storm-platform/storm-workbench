# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .compendium import compendium
from .context import context
from .deposit import deposit
from .job import execution_job
from .workflow import workflow
from .project import project
from .service import service


def register_command(ctx):
    """Register the command in a context."""
    ctx.add_command(service)

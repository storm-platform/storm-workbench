# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click

from storm_workbench.cli.graphics.aesthetic import aesthetic_traceback
from storm_workbench.workbench import Workbench


@click.group(name="service")
@click.pass_context
def service(ctx):
    """Storm WS management."""
    if ctx.obj is None:
        ctx.obj = dict()

    try:
        ctx.obj["workbench"] = Workbench()
    except:
        aesthetic_traceback(show_locals=True)

        return

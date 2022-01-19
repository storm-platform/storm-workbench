# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps

from pydash import py_


def parse_arguments_as_dict(sep=",", argument_key_value_sep="=", inject_key=None):
    """Parse string arguments as dict.

    This decorator parses arguments, encoded
    as string, to a ``kwargs`` dict arguments.

    Args:
        sep (str): Separator used to split each parameter in the string.

        argument_key_value_sep (str): Separator used to define key and value in a string.

        inject_key (str): Key used to pass the parsed value to the decored function.
    Returns:
        Callable: Parser decorator wrapper.
    """

    def parser(f):
        @wraps(f)
        def wrapper(*args, _params=None, **kwargs):
            if _params:
                # assuming that this variable is encoded in
                # the following format:
                # > "property[argument]<value>[sep]property[argument]<value>"
                # > e.g., for argument='=' and sep=',', we can parse the following string:
                # >       property=<value>,property=<value>
                _params_arguments = _params
                if sep:
                    _params_arguments = _params.split(sep)

                # mutate to a dictionary
                _params_arguments = [
                    v.split(argument_key_value_sep) for v in _params_arguments
                ]
                _params_arguments = {k: v for k, v in _params_arguments}

                if inject_key:
                    _params_arguments = {inject_key: _params_arguments}

                kwargs = py_.merge(kwargs, _params_arguments)
            return f(*args, **kwargs)

        return wrapper

    return parser

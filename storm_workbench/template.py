# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
from pathlib import Path
from typing import Union

from jinja2 import Environment, PackageLoader


def render_template(
    template_name: str, module_name: str, module_path: str, **template_objects
):
    """Render a jinja template.

    Args:
        template_name (str): Template name inside the ``module_path`` directory.

        module_name (str): Module where the template is stored.

        module_path (str): Path where the template is inside the ``module_name`` module.

        template_objects: Variables used in the template renderization.

    Returns:
        str: String with the renderized content.
    """
    env = Environment(loader=PackageLoader(module_name, module_path))

    # Metadata template file
    template = env.get_template(template_name)

    # Rendering the template and cleaning the output result.
    return template.render(**template_objects)


def write_template(
    file: Union[str, Path], template_name: str, **template_objects
) -> Path:
    """Write a jinja2 template in a file.format

    This function will render the specified Jinja2 template and save
    the rendered content in a file.

    Args:
        file (Union[str, Path]): File to write the template.

        template_name (str): Template name.

        template_objects: Variables used in the template renderization.
    Returns:
        Path: Path where the written file will be saved.
    """

    file = Path(file)

    if file.exists() and not file.is_file():
        raise ValueError(f"`{file}` must be a file!")

    with file.open("w") as ofile:
        rendered_content = render_template(
            template_name=template_name,
            module_name="storm_workbench",
            module_path="templates",
            **template_objects,
        )

        ofile.write(rendered_content)
    return file


def markdown_to_html(file: Union[str, Path]) -> Path:
    """Convert a markdown file template into a html file.

    Args:
        file (Union[str, Path]): Path to markdown file.

    Returns:
        Path: Path to html generated file.

    See:
        This function render the html using the (markdown) github flavor. To
        more information about the conversion, please check the documentation
        of the ``gh-md-to-html`` library.
    """
    file = Path(file)
    output_file = Path(f"{file.name}.html")

    if file.exists() and not file.is_file():
        raise ValueError(f"`{file}` must be a valid file!")

    # temporary (ToDo): in a near future, we will change this to
    # use the ``gh-md-to-html`` Python API.
    os.system(
        f"cd {file.parent} && gh-md-to-html {file} -c assets/styles -i assets/images"
    )
    return output_file

# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

import bagit

from storm_workbench.api.stage.exporter.base import BaseExporter


class BagItExporter(BaseExporter):
    """BagIt Exporter class.

    This class implements an Exporter using the BagIt File
    Packaging Format. For more information about the BagIt
    and its specification, please check the ``RFC 8493``
    <https://datatracker.ietf.org/doc/html/rfc8493>.
    """

    def save(self, input_dir: Path, output_file: Path, jobs=2, **kwargs) -> Path:
        # preparing the filename
        output_file = output_file.parent / output_file.name.replace(".zip", "")

        # bagit!
        bagit.make_bag(input_dir, processes=jobs, **kwargs)

        # moving the generated bagit
        # special case: for now, we are creating a zip file with
        # the bagit. In the future, the Workbench will be extended
        # to manage the Bagit itself.
        filename = shutil.make_archive(str(output_file), "zip", input_dir)

        return output_file.parent / filename

    def load(self, file: Path, output_dir: Path, jobs=2, **kwargs) -> Path:
        tmp_dir = output_dir / "tmp"
        tmp_dir.mkdir(exist_ok=True, parents=True)

        # extract and validating the BagIt.
        shutil.unpack_archive(file, tmp_dir)

        # validating
        bag = bagit.Bag(str(tmp_dir))  # nqa
        bag.validate(processes=jobs, **kwargs)

        # moving the validated files
        exported_data = tmp_dir / "data"
        copy_tree(str(exported_data), str(output_dir))

        shutil.rmtree(tmp_dir)

        return output_dir

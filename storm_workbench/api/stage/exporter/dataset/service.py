# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Union, List, Tuple

from joblib import Parallel, delayed
from pydash import py_
from storm_hasher import StormHasher

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.backstage.database.model import ExecutionCompendiumModel
from storm_workbench.api.stage.exporter.bagit import BagItExporter
from storm_workbench.api.stage.exporter.base import BaseExporterService, BaseExporter
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


def _make_path(base_uri, path, filename, path_dimensions, split_length) -> Path:
    """Generate a path as base location for a file.

     Args:
         base_uri: The base URI.

         path: The relative path.

         path_dimensions: Number of chunks the path should be split into.

         split_length: The length of any chunk.
     Returns:
         Path: A string representing the full path.

    See:
         This code was adapted from the ``Invenio-Files-Rest``. For more information, please see
         the ``Invenio-Files-Rest`` code repository: <https://github.com/inveniosoftware/invenio-files-rest/blob/563609bca4dd408532c07c50d44db80a461d21dc/invenio_files_rest/helpers.py#L195>.
    """
    import os

    assert len(path) > path_dimensions * split_length

    uri_parts = []
    for i in range(path_dimensions):
        uri_parts.append(path[0:split_length])
        path = path[split_length:]
    uri_parts.append(path)
    uri_parts.append(filename)

    return Path(os.path.join(base_uri, *uri_parts))


class DatasetExporterService(BaseExporterService):

    exporter_cls = BagItExporter
    """Exporter class."""

    def __init__(
        self,
        config: WorkbenchDefinitionFile = None,
        backstage: BackstageAccessor = None,
        exporter: BaseExporter = None,
    ):
        super(DatasetExporterService, self).__init__(config, backstage)

        self._exporter = exporter or self.exporter_cls()

    def save(
        self,
        compendia: List[Tuple[ExecutionCompendiumModel, str]],
        output_dir: Union[str, Path],
        temp_dir: Union[str, Path] = None,
        filename: str = None,
        **kwargs,
    ):
        # defining the base information
        package_name = f"{self._config.definitions.tool.storm.name}.zip"

        # defining the directories and validate them.
        output_dir = Path(output_dir)
        temp_dir = Path(temp_dir) if temp_dir else Path(tempfile.mkdtemp())

        for _dir, _name in [(temp_dir, "temp_dir"), (output_dir, "output_dir")]:
            if _dir.exists() and not _dir.is_dir():
                raise ValueError(f"`{_name}` must be a directory.")

            _dir.mkdir(exist_ok=True, parents=True)

        # organizing the compendia files.
        # at the end of script, a directory with the following structure will
        # be created:
        # - files/           (Directory with the exported files);
        # - datapackage.json (Metadata with the description required to use the files in an experiment reproduction)
        base_output_dir = "files"

        output_dir_file = temp_dir / base_output_dir
        output_file_meta = temp_dir / "datapackage.json"

        output_dir_file.mkdir(exist_ok=True, parents=True)

        # special case: in this version we will use the dataset exporter
        # only to support the users to share the data required to reproduce
        # the compendia. In the future, we will support multiple exporters.
        compendia_inputs = []
        compendia_unpacked_files = []

        for compendium, _ in compendia:
            compendia_inputs.extend(compendium.inputs)
            compendia_unpacked_files.extend(
                py_.get(compendium, "metadata.others.unpacked_files.datasources", [])
            )

        # only the input data that is not unpacked.
        files_to_pack = py_.filter(
            compendia_inputs, lambda x: x["key"] in compendia_unpacked_files
        )

        # file description: this variable is modeled as required by the Storm Core
        # to reproduce experiments with external data.
        files_description = {"checksum": {}, "files": []}

        def _validate_and_copy_callback(file):
            """callback function to validate and copy the files."""
            file_id = str(uuid.uuid4())
            file_path = Path(file["key"])
            file_hash = StormHasher(file["algorithm"]).hash_file(file_path)

            # creating a path into the package
            # rationale: we don't use the filenames to avoid
            # encoding problems.
            file_path_package_rel = _make_path(base_output_dir, file_id, "data", 2, 2)
            file_path_package_fs = temp_dir / file_path_package_rel

            if file_hash != file["checksum"]:
                raise RuntimeError(f"Invalid checksum for {file_path.name}")

            # copying the file to the temporary directory.
            file_path_package_fs.parent.mkdir(exist_ok=True, parents=True)

            shutil.copy(file_path, file_path_package_fs)

            # returning the file description.
            return {
                "checksum": (file_path.name, file_hash),
                "files": (file_path.name, str(file_path_package_rel)),
            }

        # setup a joblib worker process.
        files_description_res = Parallel(
            n_jobs=self._config.definitions.tool.storm.exporter.jobs
        )(delayed(_validate_and_copy_callback)(file) for file in files_to_pack)

        # organizing the files description
        files_description["checksum"] = {
            k: v for k, v in [p["checksum"] for p in files_description_res]
        }
        files_description["files"] = [
            {"source": k, "target": v}
            for k, v in [p["files"] for p in files_description_res]
        ]

        # saving the files description.
        with output_file_meta.open("w") as ofile:
            json.dump(files_description, ofile)

        # defining the output file
        output_file = filename or f"{package_name}-dataset"
        output_file = output_dir / output_file

        if output_file.exists():
            output_file.unlink()

        # exporting!
        output_file = self._exporter.save(
            input_dir=temp_dir,
            output_file=output_file,
            jobs=self._config.definitions.tool.storm.exporter.jobs,
        )

        if Path(tempfile.gettempdir()) in temp_dir.parents:
            shutil.rmtree(temp_dir)

        return output_file

    def load(
        self, file: Union[str, Path], output_dir: Union[str, Path], **kwargs
    ) -> Path:
        # defining the directories and validate them.
        file = Path(file)
        output_dir = Path(output_dir)

        if file.exists() and not file.is_file():
            raise ValueError(f"`{file}` must be a valid file!")

        if output_dir.exists() and not output_dir.is_dir():
            raise ValueError(f"`{file}` must be a valid directory!")

        # importing
        output_dir = self._exporter.load(
            file=file,
            output_dir=output_dir,
            jobs=self._config.definitions.tool.storm.exporter.jobs
            if self._config
            else 2,  # nqa
            **kwargs,
        )

        # updating the `data.json` path
        data_file = next(output_dir.glob("*datapackage.json"))
        if data_file:
            with Path(data_file).open("r") as ifile:
                data_file_content = json.load(ifile)

                for idx, file in enumerate(data_file_content["files"]):
                    data_file_content["files"][idx] = {
                        "source": file["source"],
                        "target": str(output_dir.absolute() / file["target"]),
                    }

                # saving the modifications
                with Path(data_file).open("w") as ofile:
                    json.dump(data_file_content, ofile)

        return output_dir

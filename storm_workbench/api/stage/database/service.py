# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from datetime import datetime

from storm_workbench.api.backstage.argparser import parse_arguments_as_dict
from storm_workbench.api.backstage.database.model import ExecutionCompendiumModel
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.exceptions import ExecutionCompendiumNotFound


class DatabaseService(BaseStageService):
    """Database service.

    This class provides a high-level API to manipulate the
    database models.
    """

    @parse_arguments_as_dict()
    def query(self, **kwargs):
        """Query the database.

        Args:
            kwargs: Arguments to filter the execution compendia.

        Returns:
            List[ExecutionCompendiumModel]: List with the founded execution compendium in the database.

        Raises:
            ExecutionCompendiumNotFound: When not found compendia with the defined criteria.

        See:
            The filter in the Execution Compendium indexed is made with the ``peewee.ModelSelect.filter``
            method. For more details about the parameters that can be used, please, check the official
            peewee documentation: <http://docs.peewee-orm.com/en/latest/peewee/api.html?highlight=filter#ModelSelect.filter>
        """
        execution_compendia = list(
            ExecutionCompendiumModel.select()
            .filter(**kwargs)
            .order_by(ExecutionCompendiumModel.created)
        )

        if not execution_compendia:
            raise ExecutionCompendiumNotFound("Execution Compendium not found!")

        return execution_compendia

    @parse_arguments_as_dict()
    def query_index(self, **kwargs):
        """Query the graph index database.

        Args:
            kwargs: Arguments to filter the execution compendia.

        Returns:
            List[Tuple[ExecutionCompendiumModel, ExecutionCompendium]]: List with the founded execution compendium and the
            indexed document.

        Raises:
            ExecutionCompendiumNotFound: When not found compendia with the defined criteria.

        See:
            The filter in the Execution Compendium indexed is made with the ``peewee.ModelSelect.filter``
            method. For more details about the parameters that can be used, please, check the official
            peewee documentation: <http://docs.peewee-orm.com/en/latest/peewee/api.html?highlight=filter#ModelSelect.filter>
        """
        execution_compendia = list(
            ExecutionCompendiumModel.select()
            .filter(**kwargs)
            .order_by(ExecutionCompendiumModel.created)
        )

        if not execution_compendia:
            raise ExecutionCompendiumNotFound("Execution Compendium not found!")

        return [
            (
                ec,
                next(
                    self._backstage.execution.index.search.query.query(
                        name=str(ec.uuid)
                    )
                )[0],
            )
            for ec in execution_compendia
        ]

    def _synchronize_records(self):
        """Synchronize the index and the database records."""
        # checking the compatibility between the database and the index.
        # rationale: in general cases, this operation
        # will be cheap, because users don't have many indexed records.
        database_compendia = ExecutionCompendiumModel.select()
        for compendium in database_compendia:
            indexed_compendium = list(
                self._backstage.execution.index.search.query.query(
                    name=str(compendium.uuid)
                )
            )

            # if the database compendium is not in the index
            # so we will remove it from the database.
            if not indexed_compendium:
                compendium.delete_instance()
                continue

            # now, we will check if the status is compatible.
            _, status = indexed_compendium[0]

            ExecutionCompendiumModel.update(
                updated=datetime.now(), status=status
            ).where(ExecutionCompendiumModel.uuid == compendium.uuid).execute()

        # saving the session modifications.
        self._backstage.session.save()

    def remove_record(self, name: str, remove_related_compendia: bool = True):
        """Remove record from the database.

        Args:
            name (str): Record name.

            remove_related_compendia (bool): Flag indicating if the related
            compendium should be deleted

        Returns:
            None: The record will be removed from the database.
        """
        # two steps process:
        #  1. remove from the index;
        #  2. remove from the database.

        # 1. removing from the index.
        record = ExecutionCompendiumModel.get(name=name)

        # deindexing!
        self._backstage.execution.index.deindex_execution(
            execution_compendium_name=str(record.uuid),
            remove_related_compendia=remove_related_compendia,
        )

        # 2. removing from the database.
        record.delete_instance()

        self._synchronize_records()

    def upsert_record(self, execution_compendium: ExecutionCompendiumModel):
        """Add (or update) a new execution compendium record.

        Args:
            execution_compendium (ExecutionCompendiumModel): Execution compendium object.

        Returns:
            ExecutionCompendiumModel: Record Object created in the database.

        Note:
            This function will try to create the record. If already exists, the
            record will be updated.
        """
        # getting the execution compendium status from the graph index.
        # note: the query ``must`` return a valid object! otherwise,
        # the execution had a problem.
        ec_index = list(
            self._backstage.execution.index.search.query.query(
                name=str(execution_compendium.uuid)
            )
        )
        ec_index = ec_index[0]

        # removing the None values.
        execution_compendium_data = dict(
            name=execution_compendium.name,
            description=execution_compendium.description,
            uuid=execution_compendium.uuid,
            status=ec_index[-1],
            command=str(execution_compendium.command),
            pid=execution_compendium.pid,
        )
        execution_compendium_data = {
            k: v for k, v in execution_compendium_data.items() if v is not None
        }

        # trying to update an already exists compendium
        update_status = (
            ExecutionCompendiumModel.update(
                updated=datetime.now(), **execution_compendium_data
            )
            .where(ExecutionCompendiumModel.uuid == execution_compendium.uuid)
            .execute()
        )

        if not update_status:  # create a new record
            record = ExecutionCompendiumModel.create(**execution_compendium_data)
        else:
            record = ExecutionCompendiumModel.get(
                ExecutionCompendiumModel.uuid == execution_compendium.uuid
            )

        self._synchronize_records()
        return record

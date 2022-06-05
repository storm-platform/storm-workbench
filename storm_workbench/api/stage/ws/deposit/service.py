# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_client.models.deposit import DepositJob, DepositJobList, DepositJobServiceList

from storm_workbench.api.backstage.accessor import BackstageAccessor
from storm_workbench.api.backstage.argparser import parse_arguments_as_dict
from storm_workbench.api.stage.base import BaseStageService
from storm_workbench.api.stage.ws.decorator import pass_project_context
from storm_workbench.api.stage.ws.service import BaseContextualizedService
from storm_workbench.workbench.settings import WorkbenchDefinitionFile


class DepositService(BaseContextualizedService):
    """Deposit service class.

    This class provides methods to use and manage the Deposit
    resources from the Storm WS.
    """

    @pass_project_context
    def __init__(
        self,
        config: WorkbenchDefinitionFile = None,
        backstage: BackstageAccessor = None,
        context: BaseStageService = None,
    ):
        """Initializer.

        Args:
            config (WorkbenchDefinitionFile): Workbench configuration.

            backstage (BackstageAccessor): Accessor object to manipulate the Backstage API (Workbench low-level API).

            context (BaseStageService): Service which defines the context.
        """
        super(DepositService, self).__init__(config, backstage, context)

    def create(self, deposit: DepositJob):
        """Create a new Deposit in the Storm WS.

        Args:
            deposit (Deposit): Deposit object.

        Returns:
            Deposit: Deposit object created in the Storm WS.
        """
        created_deposit = self._context.deposit.create(deposit)

        return created_deposit

    def describe(self, id_: str, **kwargs) -> DepositJob:
        """Describe a Storm WS Deposit.

        Args:
            id_ (str): Deposit Identifier.

            kwargs: Extra parameters to the HTTP request library.

        Returns:
            Deposit: Deposit Object.
        """
        return self._context.deposit.get(id_, **kwargs)

    @parse_arguments_as_dict(sep=",", argument_key_value_sep="=", inject_key="json")
    def start(self, id_: str, **kwargs) -> DepositJob:
        """Start a Storm WS Deposit proces.

        Args:
            id_ (str): Deposit Identifier.

            kwargs: Extra parameters to the HTTP request library.

        Returns:
            Deposit: Deposit Object.
        """
        return self._context.deposit.start_deposit(id_, request_options=kwargs)

    def update(self, deposit: DepositJob):
        """Update a Deposit in the Storm WS.

        Args:
            deposit (Deposit): Deposit object.

        Returns:
            Deposit: Deposit object updated in the Storm WS.
        """
        selected_deposit = self._context.deposit.get(deposit.id)

        # monkey patch to update the properties.
        for attr in ["service", "pipelines"]:
            attr_val = getattr(deposit, attr)

            if attr_val:  # avoiding consistency problems
                setattr(selected_deposit, attr, attr_val)

        # saving the modifications
        return self._context.deposit.save(selected_deposit)

    def delete(self, id_: str):
        """Delete a Deposit from the Storm WS.

        Args:
            id_ (str): Deposit Identifier.

        Returns:
            None: The Deposit will be deleted from the Storm WS.
        """
        self._context.deposit.delete(id_)

    def services(self, **kwargs) -> DepositJobServiceList:
        """List the available services to Deposit.

        Args:
            kwargs: Extra parameters to the HTTP request library.

        Returns:
            DepositServiceList: List with available deposit services.
        """
        return self._context.deposit.list_services(**kwargs)

    @parse_arguments_as_dict(sep="&", argument_key_value_sep=":")
    def search(self, **kwargs) -> DepositJobList:
        """Search for deposit requests in the Storm WS.

        Args:
            kwargs: Extra arguments to search method.

        Returns:
            DepositList: List with the founded Deposits.
        """
        return self._context.deposit.search(**kwargs)

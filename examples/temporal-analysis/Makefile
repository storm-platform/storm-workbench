# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

step_1:
	@echo "Running experiment"
	workbench exec run --name step-1 python analysis/01_generate-ndwi.py

	@echo "Uploading data to Storm WS"
	workbench service compendium draft-new --source "step-1"
	workbench service compendium files-upload --source "step-1"

step_2:
	@echo "Running experiment"
	workbench exec run --name step-2 python analysis/02_extract-time-series.py

	@echo "Uploading data to Storm WS"
	workbench service compendium draft-new --source "step-2"
	workbench service compendium files-upload --source "step-2"

step_3:
	@echo "Running experiment"
	workbench exec run --name step-3 python analysis/03_visualizing-time-series.py

	@echo "Uploading data to Storm WS"
	workbench service compendium draft-new --source "step-3"
	workbench service compendium files-upload --source "step-3"

produce-result: step_1 step_2 step_3

publish:
	 workbench service compendium draft-publish --id $(C1)
	 workbench service compendium draft-publish --id $(C2)
	 workbench service compendium draft-publish --id $(C3)

workflow:
	# Create a workflow
	workbench service workflow create \
		--id $(W1) \
		--title "Temporal Analysis Workflow" \
		--description "Temporal Analysis workflow" \
		--version "v1.0"

	# Adding compendia to the workflow
	workbench service workflow add-compendium \
		--workflow-id $(W1) \
		--compendium-id $(C1)

	workbench service workflow add-compendium \
		--workflow-id $(W1) \
		--compendium-id $(C2)

	workbench service workflow add-compendium \
		--workflow-id $(W1) \
		--compendium-id $(C3)

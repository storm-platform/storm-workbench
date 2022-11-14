# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

SHELL := /bin/bash

#
# Low-Level commands
#
step_0:
	python3 -m venv venv

	source venv/bin/activate \
		&& pip install poetry \
		&& pip install --upgrade pip \
		&& pip install .	

step_1:
	@echo "Running experiment"
	source venv/bin/activate \
		&& workbench exec run \
		--name "(Step 1) NDWI processing" \
		--description "Processing data cube (in RasterBrick format) to generate a NDWI Data Cube" \
		python analysis/01_generate-ndwi.py

	@echo "Uploading data to Storm WS"
	source venv/bin/activate \
		&& workbench service compendium draft-new --source "(Step 1) NDWI processing" \
		&& workbench service compendium files-upload --source "(Step 1) NDWI processing"

step_2:
	@echo "Running experiment"
	source venv/bin/activate \
		&& workbench exec run \
		  --name "(Step 2) Extracting NDWI Time Series" \
		  --description "Extracting time series from NDWI Data Cubes (in RasterBrick format)" \
  		  python analysis/02_extract-time-series.py

	@echo "Uploading data to Storm WS"
	source venv/bin/activate \
		&& workbench service compendium draft-new --source "(Step 2) Extracting NDWI Time Series" \
		&& workbench service compendium files-upload --source "(Step 2) Extracting NDWI Time Series"

step_3:
	@echo "Running experiment"
	source venv/bin/activate \
		&& workbench exec run \
		  --name "(Step 3) Visualizing NDWI Time Series" \
		  --description "Visualizing Time Series data extracted from NDWI Data Cubes." \
		  python analysis/03_visualizing-time-series.py

	@echo "Uploading data to Storm WS"
	source venv/bin/activate \
		&& workbench service compendium draft-new --source "(Step 3) Visualizing NDWI Time Series" \
		&& workbench service compendium files-upload --source "(Step 3) Visualizing NDWI Time Series"

#
# High-Level commands
#
exe-experiment-prepare-environment: step_0 ## Prepare environment to run the experiment

exe-experiment-execution: step_1 step_2 step_3  ## Execute the experiment.

exe-experiment-publish:  ## Publish the experiment in the Storm WS.
	source venv/bin/activate \
		&& workbench service compendium draft-publish --id $(C1) \
		&& workbench service compendium draft-publish --id $(C2) \
		&& workbench service compendium draft-publish --id $(C3)

workflow-create:  ## Create a new workflow based on the steps executed during the experiment.
	# Create a workflow
	source venv/bin/activate \
		&& workbench service workflow create \
		--id $(W1) \
		--title "Temporal Analysis Workflow" \
		--description "Temporal Analysis workflow" \
		--version "v1.0"

	# Adding compendia to the workflow
	source venv/bin/activate \
		&& workbench service workflow add-compendium \
		--workflow-id $(W1) \
		--compendium-id $(C1)

	source venv/bin/activate \
		&& workbench service workflow add-compendium \
		--workflow-id $(W1) \
		--compendium-id $(C2)

	source venv/bin/activate \
		&& workbench service workflow add-compendium \
		--workflow-id $(W1) \
		--compendium-id $(C3)

workflow-execution-create:   ## Create a execution context for the Workflow
	source venv/bin/activate \
		&& workbench service execution create \
		--workflow-id $(W1) \
		--service execution-reprozip-serial

workflow-execution-execute:   ## Execute a Workflow
	source venv/bin/activate \
		&& workbench service execution start \
		--id $(E1) \
		--args reana_access_token=$(R1)

checksum:  ##  Generate compendium files checksum
	rm -rf checksums && mkdir -p checksums

	find . -type f -exec md5sum {} > checksums/md5sums.txt \;
	find . -type f -exec sha256sum {} > checksums/sha256sums.txt \;
	find . -type f -exec sha512sum {} > checksums/sha512sums.txt \;

#
# Documentation function (thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
#
help:  ## Show this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

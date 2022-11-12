# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

execute:  ## Execute the experiment
	micromamba run -n fmask \
		workbench exec run \
			--name "Fmask example using Storm workbench" \
			--description "Reproducible Fmask using Storm workbench" \
			./run.sh
	
	micromamba run -n fmask \
		workbench export compendium -o data/derived_data/execution-compendium


save-online:  # Save experiment data into the Storm WS
	micromamba run -n fmask \
		workbench service compendium draft-new --source "Fmask example using Storm workbench"

	micromamba run -n fmask \
		workbench service compendium files-upload --source "Fmask example using Storm workbench"


clean:  ## Delete the experiments results
	rm -rf data/derived_data/*.tif


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

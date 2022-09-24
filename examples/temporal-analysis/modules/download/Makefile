# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Gallery.
#
# storm-gallery is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

checksum:  ##  Generate files checksum
	mkdir -p checksums

	find . -name "*.tif" -type f -exec md5sum {} > checksums/md5sums.txt \;
	find . -name "*.tif" -type f -exec sha256sum {} > checksums/sha256sums.txt \;
	find . -name "*.tif" -type f -exec sha512sum {} > checksums/sha512sums.txt \;


#
# Documentation function (thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
#
help:  ## Show this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

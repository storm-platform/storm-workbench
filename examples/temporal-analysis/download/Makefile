# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Gallery.
#
# storm-gallery is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

checksum:
	find . -name "*.tif" -type f -exec md5sum {} > checksums/md5sums.txt \;
	find . -name "*.tif" -type f -exec sha256sum {} > checksums/sha256sums.txt \;
	find . -name "*.tif" -type f -exec sha512sum {} > checksums/sha512sums.txt \;

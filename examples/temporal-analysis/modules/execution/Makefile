# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

reana-start-workflow:  ## Initialize the workflow created by Storm Workbench on a Reana Cluster
	reana-client start -w $(WF1)

#
# Documentation function (thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html)
#
help:  ## Show this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

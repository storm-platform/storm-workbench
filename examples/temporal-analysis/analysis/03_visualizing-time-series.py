# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-workbench is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import pandas as pd
from plotnine import *

from pathlib import Path

#
# General definitions
#

# Input data
table_input = Path("data/derived_data/sample-water-timeseries.csv")

# Output figure
figure_output = Path("data/derived_data/timeseries-visualization.png")

#
# 1. Reading the data
#
table_data = pd.read_csv(table_input)

#
# 2. Transforming the data to plot
#
table_data = table_data.melt("Unnamed: 0")
table_data.columns = ["time_index", "variable", "value"]

#
# 3. Plotting data
#
plot = ggplot(table_data, aes(x="time_index", y="value")) + geom_line()

ggsave(plot, filename=figure_output)

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
table_data = pd.read_csv(table_input, index_col='Unnamed: 0')

#
# 2. Transforming the data to plot
#

# 2.1. Creating the date column (based on the downloaded data)
table_data["time"] = pd.date_range("2018-08-29", "2019-09-13", freq="16D")

# 2.2. Tidying the data!
table_data = table_data.melt("time")
table_data.columns = ["time", "point", "value"]

#
# 3. Plotting data
#
plot = (
    ggplot(table_data, aes(x="time", y="value", group="point"))
        + geom_line(color="black")
        + xlab("Time")
        + ylab("NDWI")
        + theme_bw()
        + theme(axis_text_x = element_text(angle = 20))
        + scale_x_date(date_labels = "%b/%Y")
        + ggtitle("NDWI Time Series (CBERS-4A/AWFI)")
)

ggsave(plot, filename=figure_output)

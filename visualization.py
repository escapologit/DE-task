"""
Visualize the number of shipments that go into the US (from non-US locations) 
and leave the US (to non-US locations) for each month that the sample data covers. 

First version of this script was using Matplotlib for visualization. (result: monthly_shipments_matplotlib.png)
For purpose of interactive visualization, this final version is using Plotly. (result: monthly_shipments_plotly.html)
"""

from parse_files import parse_files
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import datetime

# parse csv files
path = './data'
df = parse_files(path)

# sort by event time and shipment ID
df['EventTime'] = pd.to_datetime(df['EventTime'])	
df = df.sort_values(['ShipmentID', 'EventTime'])

# group by shipment ID
df = df.groupby('ShipmentID').agg({
    'OriginCountry': 'first',
    'DestinationCountry': 'last',
    'EventTime': ['min', 'max']
}).reset_index()

# flatten multiindex
df.columns = ['_'.join(col).strip('_') for col in df.columns.values]

# filter shipments that go from US to non-US locations
from_us = df[(df['OriginCountry_first'] == 'US') & (df['DestinationCountry_last'] != 'US')]
from_us['YearMonth'] = from_us['EventTime_min'].dt.to_period('M')
from_us.drop(['EventTime_min', 'EventTime_max'], axis=1, inplace=True)
# filter shipments that go from non-US locations to US
to_us = df[(df['OriginCountry_first'] != 'US') & (df['DestinationCountry_last'] == 'US')]
to_us['YearMonth'] = to_us['EventTime_max'].dt.to_period('M')
to_us.drop(['EventTime_min', 'EventTime_max'], axis=1, inplace=True)

from_us = from_us.groupby('YearMonth').size().reset_index(name='Count_from_us')
to_us = to_us.groupby('YearMonth').size().reset_index(name='Count_to_us')

df = pd.merge(from_us, to_us, on='YearMonth')


# unique labels for year and month
unique_years = sorted(df['YearMonth'].dt.year.astype(str).unique())
unique_months = sorted(df['YearMonth'].dt.strftime('%m').unique())

# trying interactive plotting using plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['YearMonth'].astype(str), y=df['Count_from_us'],
    mode='lines+markers', name='From US'
))
fig.add_trace(go.Scatter(
    x=df['YearMonth'].astype(str), y=df['Count_to_us'],
    mode='lines+markers', name='To US'
))


# add dropdown filters for year and month

year_buttons = []
for year in unique_years:
    filtered = df[df['YearMonth'].dt.year.astype(str) == year]
    year_buttons.append(dict(
        label=year,
        method="update",
        args=[
            {
                "x": [filtered['YearMonth'].astype(str), filtered['YearMonth'].astype(str)],
                "y": [filtered['Count_from_us'], filtered['Count_to_us']]
            },
            {
                "title.text": f"Monthly shipments in {year}",
                "xaxis.tickformat": "%b",
                "xaxis.dtick": "M1"
            }
        ]
    ))

month_buttons = []
for month in unique_months:
    filtered = df[df['YearMonth'].dt.strftime('%m') == month]
    month_name = datetime.datetime.strptime(month, '%m').strftime('%B')
    month_buttons.append(dict(
        label=month,
        method="update",
        args=[
            {
                "x": [filtered['YearMonth'].astype(str), filtered['YearMonth'].astype(str)],
                "y": [filtered['Count_from_us'], filtered['Count_to_us']]
            },
            {
                "title.text": f"Shipments in {month_name} across years",
                "xaxis.tickformat": "%Y",
                "xaxis.dtick": "M12"
            }
        ]
    ))

fig.update_layout(
    updatemenus=[
        dict(
            buttons=year_buttons,
            direction="down",
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.2,
            yanchor="top"
        ),
        dict(
            buttons=month_buttons,
            direction="down",
            showactive=True,
            x=0.4,
            xanchor="left",
            y=1.2,
            yanchor="top"
        )
    ],
    annotations=[
        dict(text="Filter by Year:", x=0, xref="paper", y=1.2, yref="paper", showarrow=False),
        dict(text="Filter by Month:", x=0.35, xref="paper", y=1.2, yref="paper", showarrow=False)
    ],
    title="Monthly shipments To and From US",
    xaxis_title="Year-Month",
    yaxis_title="Number of shipments",
    hovermode='x unified',
    template='plotly_white'
)

fig.show()
fig.write_html("monthly_shipments_plotly.html")
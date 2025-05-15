"""
Visualize the number of shipments that go into the US (from non-US locations) 
and leave the US (to non-US locations) for each month that the sample data covers.
"""

from parse_files import parse_files
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
from_us['YearMonth'] = from_us['EventTime_min'].dt.to_period('M').astype(str)
from_us.drop(['EventTime_min', 'EventTime_max'], axis=1, inplace=True)
# filter shipments that go from non-US locations to US
to_us = df[(df['OriginCountry_first'] != 'US') & (df['DestinationCountry_last'] == 'US')]
to_us['YearMonth'] = to_us['EventTime_max'].dt.to_period('M').astype(str)
to_us.drop(['EventTime_min', 'EventTime_max'], axis=1, inplace=True)

from_us = from_us.groupby('YearMonth').size().reset_index(name='Count_from_us')
to_us = to_us.groupby('YearMonth').size().reset_index(name='Count_to_us')

# plotting
plt.figure(figsize=(15, 6))
plt.plot()
plt.plot(from_us['YearMonth'], from_us['Count_from_us'], linewidth=2, marker='o', label='From US')
plt.plot(to_us['YearMonth'], to_us['Count_to_us'], linewidth=2, marker='o', label='To US')

plt.xticks(rotation=45)
plt.xlabel('Year-Month')
plt.ylabel('Number of shipments')
plt.title('Monthly shipments To and From US')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('monthly_shipments.png')
plt.show()
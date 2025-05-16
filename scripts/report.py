"""
Generate a new report that will, for every shipment, contain the shipment's origin, 
destination, total number of packages, the total time it took the shipment to arrive at its destination, 
the total weight of the shipment, and the total cost of the shipment.
"""

from parse_files import parse_files
import pandas as pd
import pycountry
from currency_converter import CurrencyConverter
from babel.numbers import get_territory_currencies
from datetime import datetime

# parse csv files
path = './data'
df = parse_files(path)

# sort by event time and shipment ID
df['EventTime'] = pd.to_datetime(df['EventTime'])	
df = df.sort_values(['ShipmentID', 'EventTime'])


# get country currency
def get_country_currency(country):
    """
    Get currency from country name. 
    
    Account for special cases:
        - AED: fixed exchange rate of 1 AED = 0.27 USD
        - UK: use GB
    """
    try:
        curr = get_territory_currencies(country)[0]
        if curr == 'AED':
            return 'USD' # default, I'll fix it below
        return curr
    except:
        if country == "UK":
            country = "GB"
        return get_territory_currencies(country)[0]


# currency conversion from DestinationCountry currency to USD
final_currency = 'USD'
c = CurrencyConverter(fallback_on_missing_rate=True)
# c.convert(cost, from, to, date)
df['Cost'] = df.apply(lambda row: c.convert(row['Cost'], get_country_currency(row['DestinationCountry']), final_currency, row['EventTime'].date()), axis=1)

# fix AED to USD
# "Since 1997, the dirham has been pegged to the US dollar at a rate of 1 USD = 3.6725 AED."
df['Cost'] = df.apply(lambda row: (row['Cost'] / 3.6725) if row['DestinationCountry'] == 'AE' else row['Cost'], axis=1)


# group by shipment ID
df = df.groupby('ShipmentID').agg({
    'Origin': 'first',
    'Destination': 'last',
    'PackageID': 'nunique',
    'EventTime': ['min', 'max'],
    'Weight': 'sum',
    'Cost': 'sum'
}).reset_index()

# flatten multiindex
df.columns = ['_'.join(col).strip('_') for col in df.columns.values]

df['TimeTotal'] = (df['EventTime_max'] - df['EventTime_min'])

# generate new report
new_report_cols = ['ShipmentID', 'Origin', 'Destination', 'PackagesTotal', 'WeightTotal', 'CostTotal(USD)', 'TimeTotal']
new_report = df.drop(columns=['EventTime_min', 'EventTime_max'])
new_report.columns = new_report_cols
print(new_report)
new_report.to_csv('report.csv', index=False)
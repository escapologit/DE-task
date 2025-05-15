"""
Infer the route a shipment from Los Angeles would take to reach Doncaster 
using a directed graph.
"""

from parse_files import parse_files
import pandas as pd
import networkx as nx

# parse csv files
path = './data'
df = parse_files(path)


G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_edge(row['Origin'], row['Destination'])

try:
    route = nx.shortest_path(G, source='Los Angeles', target='Doncaster')
    print("Route from LA to Doncaster:")
    print(" → ".join(route))
except nx.NetworkXNoPath:
    print("The route is not possible.")
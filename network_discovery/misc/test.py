import ipaddress
import networkx as nx
import matplotlib.pyplot as plt
import os
from pysnmp.hlapi import *

G = nx.Graph()
  
# To add a node
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(7)
G.add_node(9)

G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(1, 4)
G.add_edge(1, 5)

nx.draw(G)
plt.savefig("filename.png")
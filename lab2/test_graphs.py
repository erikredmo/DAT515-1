#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:41:03 2021

@author: adinahellstrom
"""

from graphs import *


from hypothesis.strategies import text
from hypothesis import given, strategies as st

import networkx as nx



###### TO TEST ################


# if (a, b) is in edges(), both a and b are in vertices()

# generate small integers, 0...10
smallints = st.integers(min_value=0, max_value=10)
# generate pairs of small integers
twoints = st.tuples(smallints, smallints)
# generate lists of pairs of small integers where x != y for each pair (x, y)
st_edge_list = st.lists(twoints, unique_by=(lambda x: x[0], lambda x: x[1]))
@given(st_edge_list)
def test_edges_vertices(a, b):
    boolean_value = False
    G = graphs.Graph(st_edge_list)
    if (a,b) in G.edges():
        if a in G.vertices() and b in G.vertices():
            boolean_value = True
    assert boolean_value == True



# if (a, b) is an edge, so is also (b, a)
@given(st_edge_list)
def test_is_edges_both_way(a, b):
    boolean_value = False
    G = graphs.Graph(st_edge_list)
    if (a, b) in G.edges():
        if (b, a) in G.edges():
            boolean_value = True
    assert boolean_value == True



'''

# shortest path algorithm
def test_shortest_path_algoritm():
    pass

'''
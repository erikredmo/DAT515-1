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


'''

@given(st.integers(), st.integers())
def test_ints_are_commutative(x, y):
    assert x + y == y + x


@given(x=st.integers(), y=st.integers())
def test_ints_cancel(x, y):
    assert (x + y) - y == x


@given(st.lists(st.integers()))
def test_reversing_twice_gives_same_list(xs):
    # This will generate lists of arbitrary length (usually between 0 and
    # 100 elements) whose elements are integers.
    ys = list(xs)
    ys.reverse()
    ys.reverse()
    assert xs == ys


@given(st.tuples(st.booleans(), st.text()))
def test_look_tuples_work_too(t):
    # A tuple is generated as the one you provided, with the corresponding
    # types in those positions.
    assert len(t) == 2
    assert isinstance(t[0], bool)
    assert isinstance(t[1], str)


@given(text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s


def test_ints_are_commutative(x, y):
    assert x - y == y - x
    
test_ints_are_commutative = given(st.integers(),
st.integers())(test_ints_are_commutative)


print(test_ints_are_commutative())



# generate small integers, 0...10
smallints = st.integers(min_value=0, max_value=10)
# generate pairs of small integers
twoints = st.tuples(smallints, smallints)
# generate lists of pairs of small integers
# where x != y for each pair (x, y)
st_edge_list = st.lists(twoints, unique_by=(lambda x: x[0], lambda x: x[1]))

@given(st_edge_list)
def test_searches(eds):
    G = Graph()
    for (a,b) in eds:
        G.add_edge(a, b)
    root = eds[0][0]
    assert breadth_first(G, root) == depth_first(G, root)
    
assert set(breadth_first(G, root)) == set(depth_first(G, root))

'''

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

print(test_edges_vertices(st_edge_list[0], st_edge_list[1]))




# if (a, b) is an edge, so is also (b, a)
@given(st_edge_list)
def test_is_edges_both_way(a, b):
    boolean_value = False
    G = graphs.Graph(st_edge_list)
    if (a, b) in G.edges():
        if (b, a) in G.edges():
            boolean_value = True
    assert boolean_value == True

test_is_edges_both_way()



# shortest path algorithm
def test_shortest_path_algoritm():
    pass

#TEST TEST
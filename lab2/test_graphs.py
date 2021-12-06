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


from tramdata import *





    # generate small integers, 0...10
smallints = st.integers(min_value=0, max_value=10)
    # generate pairs of small integers
twoints = st.tuples(smallints, smallints)
    # generate lists of pairs of small integers where x != y for each pair (x, y)
st_edge_list = st.lists(twoints, unique_by=(lambda x: x[0], lambda x: x[1]))
    
"if (a, b) is in edges(), both a and b are in vertices()"
@given(st_edge_list)
def test_edges_vertices(eds): # När man ger den en @given spelar det ingen roll vad inputen heter för den fattar att det är den givna den ska ta in
    G = Graph(eds)
    #kolla alla edges
    print('edges: ', G.edges())
    print('vertices: ', G.vertices())
    for edge in G.edges():
        assert edge[0] in G.vertices() and edge[1] in G.vertices()


"if a has b as its neighbour, then b has a as its neighbour"
@given(st_edge_list)
def test_neighbours(eds):
    print('edges: ', eds)
    bv = False
    G = Graph(eds)
    print('redadj: ', G._redadjlist)
    for edge in eds: #(0, 1)
        print('grannar till 0: ', G.neighbours(edge[0]))
        print('grannar till 1: ', G.neighbours(edge[1]))
        if edge[0] in G.neighbours(edge[1]):
            if edge[1] in G.neighbours(edge[0]):
                bv = True
        
        
        assert edge[0] in G.neighbours(edge[1]) and edge[1] in G.neighbours(edge[0])
        
        #assert bv == True


################## WITH NETWORKX #########################

import random
" shortest path algorithm "
@given(st_edge_list)
def test_shortest_path_algoritm(eds):
    if len(eds) == 0:
        print('eds is empty')
    #G1 = Graph(eds)
    G1_w = WeightedGraph(eds)
    for edge in eds:
        G1_w.set_weight(edge[0], edge[1], 1)
    
    
    G2 = nx.Graph()
    for edge in eds:
        G2.add_edge(edge[0], edge[1], weight=1)
    
    source = eds[0][0]
    target = eds[-1][-1]
    print('source', source, 'target', target)
    print(eds)
    print(dijkstra(G1_w, source)[target])
    
    assert dijkstra(G1_w, source)[target] == nx.dijkstra_path(G2, source, target, weight=1)


@given(st_edge_list)
def test_edges_vertices_nx(eds):
    G1 = Graph(eds)
        
    #för att få två likadana graphs
    G2 = nx.Graph()
    for edge in eds:
        G2.add_edge(edge[0], edge[1]) 
            
    for edge in G1.edges():
        assert edge in G2.edges() and edge[0] in G2.nodes() and edge[1] in G2.nodes()
        
    
@given(st_edge_list)
def test_neighbours_nx(eds):
    G1 = Graph(eds)
    G2 = nx.Graph()
    for edge in eds:
        G2.add_edge(edge)
        
    for edge in eds:
        assert edge[0] in G1.neighbours(edge[1]) == edge[0] in nx.neighbors(G2, edge[0]) and edge[1] in G1.neighbours(edge[0]) == edge[0] in nx.neighbors(G2, edge[1])
        
        

#test_edges_vertices()
test_shortest_path_algoritm()
test_neighbours()
test_edges_vertices_nx()
test_neighbours_nx()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:18:45 2021

@author: adinahellstrom
"""



class Graph:
    def __init__(self, edgelist, start=None, values={}, directed=False):
        self._adjlist = {}
        self._valuelist = values
        self._isdirected = directed # False => undirected
    def __len__(self):
        pass
    def add_edge(self, v1, v2):
        self._adjlist.update()
    def add_vertex(self, v):
        pass
    def edges(self):
        pass
    def get_vertex_value(self):
        pass
    def neighbours(self, v):
        pass
    def remove_edge(self, v1, v2):
        pass
    def set_vertex_value(self, v, x):
        pass
    def vertices(self):
        pass
    
class WeighthedGraph:
    def __init__(self):
        pass
    def get_weight(self, v1, v2):
        pass
    def set_weight(self, v1, v2, w):
        pass
    
        
# in graphs.py

#dijkstra(graph, source, cost=lambda u,v: 1)
#visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot')

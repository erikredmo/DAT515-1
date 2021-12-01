#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:18:45 2021

@author: adinahellstrom
"""


class Graph:
    def __init__(self, edgelist, start=None, values=None, directed=False):
        self._adjlist = {}
        if values is None:
            values = {}
        self._valuelist = values #values of nodes
        self._isdirected = directed # False => undirected
        
# plus some code for building a graph from a ’start’ object
# such as a list of edges
        
        self._adjlist = Graph.edges2adjacency(edgelist)

    def edges2adjacency(edges):

        def add_edge(adj,src,dst):
            if not src in adj:
                adj[src] = [dst]
            else:
                adj[src].append(dst)

        adj = {}
        for (src,dst) in edges:
            add_edge(adj, src, dst)
            add_edge(adj, dst, src)

        return adj

    def __len__(self):
        return len(self._adjlist)
    def add_edge(self, a, b):
        
        if a not in self._adjlist:
            #self._adjlist[a] = set() # The set() function creates a set object.
            self._adjlist[a] = [b]
        else:
            if b not in self._adjlist[a]:
                self._adjlist[a].append(b)
        
        if b not in self._adjlist:
            #self._adjlist[b] = set()
            self._adjlist[b] = [a]
        else:
            if a not in self._adjlist[b]:
                self._adjlist[b].append(a)
        # The set add() method adds a given element to a set if the element is not present in the set.
    
        
    
    def add_vertex(self, v):
        self._adjlist[v] = set()
    def edges(self):
        new_edgelist = []
        for key in self._adjlist:
            for element in self._adjlist[key]:
                new_edgelist.append((key, element))
        return new_edgelist
    def get_vertex_value(self, v):
        index = list(self._valuelist.keys()).index(v)
        return list(self._adjlist.keys())[index]
    def neighbours(self, v):
        neighbour_list = []
        for element in self._adjlist[v]:
            neighbour_list.append(element[0])
        return neighbour_list
    
    def remove_edge(self, a, b):
        for i in range(len(self._adjlist)):
            for j in range(len(self._adjlist[i])):
                if self._adjlist[i] == a and self._adjlist[i][j][0] == b:
                    self._adjlist[i][j].remove()

    def set_vertex_value(self, v, x):
        "destructive update of value"
        self._valuelist[v] = x #we don't care about the old value
    def vertices(self):
        return self._adjlist.keys()
    
class WeightedGraph(Graph):
    "If you use a native implementation, the simplest solution is probably to have a separate dictionary."
    
    def __init__(self, edgelist):
        super().__init__(edgelist) #här skapas den vanliga graphen
        self._weightlist = self._adjlist
        
    def get_weight(self, a, b):
        for element in self._adjlist[a]:
            if element[0] == b:
                return element[1]

    def set_weight(self, a, b, w):
        self._adjlist[a][self._adjlist[a].index(b)] = (b, w)


import sys

def dijkstra(graph, source, cost=lambda u,v: 1):
    unvisited_v = list(graph.vertices())
    
    # We'll use this dict to save the cost of visiting each v and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a v found so far
    previous_v = {}
    
    # We'll use max_value to initialize the "infinity" value of the unvisited vs   
    max_value = sys.maxsize
    for v in unvisited_v:
        shortest_path[v] = max_value
    # However, we initialize the starting v's value with 0   
    shortest_path[source] = 0
    # The algorithm executes until we visit all v
    while unvisited_v: # for v in unvisited_v?
        # The code block below finds the v with the lowest score
        current_min_v = None
        for v in unvisited_v: # Iterate over the vs
            if current_min_v == None:
                current_min_v = v
            elif shortest_path[v] < shortest_path[current_min_v]:
                current_min_v = v
        
        # The code block below retrieves the current v's neighbors and updates their distances
        neighbours = graph.neighbours(current_min_v)
        for neighbour in neighbours:
            prel_value = shortest_path[current_min_v] + graph.get_weight(current_min_v, neighbour)
            if prel_value < shortest_path[neighbour]:
                shortest_path[neighbour] = prel_value
                # We also update the best path to the current v
                previous_v[neighbour] = current_min_v
 
        # After visiting its neighbors, we mark the v as "visited"
        unvisited_v.remove(current_min_v)
    
    return previous_v, shortest_path
        

import graphviz

def visualize(graph): #, view='dot', name='mygraph', nodecolors={}, engine='dot'
    dot = graphviz.Graph(engine='dot')
    for v in graph.vertices():
        dot.node(str(v))
    for (a,b) in graph.edges():
        dot.edge(str(a), str(b))
    dot.render('mygraph', view='dot')

def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]['path']
    print(path)
    colormap = {str(v): 'orange' for v in path}
    print(colormap)
    visualize(G, view='view', nodecolors=colormap)


def demo():
    edgelist_demo = [(1,2),(1,3),(1,4),(3,4),(3,5),(3,6),(3,7),(6,7)]

    G = WeightedGraph(edgelist_demo)
    c = 1
    for i in range(len(edgelist_demo)):
        G.set_weight(edgelist_demo[i][0], edgelist_demo[i][1], c)
        G.set_weight(edgelist_demo[i][1], edgelist_demo[i][0], c)

        c += 1
        
    print(G._weightlist)
        
    view_shortest(G, 2, 6)

if __name__ == '__main__':
    demo()

'''
edges = [(1,2), (1,3), (2,4), (2,5), (3, 6), (3, 7), (7, 3)]

def demo():
    T = Graph(edges)
    T.add_edge(1, 7)
    T.add_edge(1, 8)
    T.add_edge(2, 8)
    print(T._adjlist)
    visualize(T)
  '''  
if __name__ == '__main__':
    demo()  

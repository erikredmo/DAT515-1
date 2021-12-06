#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:41:23 2021

@author: adinahellstrom
"""

from graphs import *


from hypothesis.strategies import text
from hypothesis import given, strategies as st
import networkx as nx
from tramdata import *
from trams import *
import collections as co

"Some of the tests from Lab 1 are also relevant here, now performed on the TramNetwork class and its methods."
"You can try to generate data for them from the stop and line lists by using hypothesis."


TRAM_FILE = '/Users/adinahellstrom/Documents/GitHub/DAT515/labb1/tramnetwork_new.json'


with open(TRAM_FILE) as trams:
    tramdict = json.loads(trams.read())
stopdict = tramdict['stops']
linedict = tramdict['lines']
timedict = tramdict['times']

st_a_stop = st.sampled_from(sorted(stopdict.keys()))
@given(st_a_stop)
def test_stops_exist(stop):
    TNW = readTramNetwork(TRAM_FILE)
    
    assert stop in TNW.all_stops()
    
    
st_a_line = st.sampled_from(sorted(linedict.keys())) 
@given(st_a_line)    
def test_lines_included(line):
    TNW = readTramNetwork(TRAM_FILE)
    
    assert line in TNW.all_lines()


st_two_stops = st.tuples(st.sampled_from(list(stopdict.keys())), st.sampled_from(list(stopdict.keys())))
@given(st_two_stops)
def test_feasible_distance(st_two_stops):
    print(st_two_stops)
    TNW = readTramNetwork(TRAM_FILE)
    D = TNW.geo_distance(stopdict, st_two_stops[0], st_two_stops[1])
    assert D <= 20000

def BFS(G, node, goal=lambda n: False):
    Q = co.deque()
    explored = [node]
    Q.append(node)
    while Q:
        v = Q.popleft()
        if goal(v):
            return v 
        for w in G.neighbours(v): #successors == neighbours
            if w not in explored:
                explored.append(w)
                Q.append(w)
    return explored
    
st_a_stop = st.sampled_from(sorted(stopdict.keys()))
@given(st_a_stop)
def test_connectedness(root_stop):
    TNW = readTramNetwork(TRAM_FILE)
    print('TNW.all_stops()', TNW.all_stops())
    print('len TNM', len(TNW.all_stops()))
    print('root', root_stop)
    explored = BFS(TNW, root_stop)
    print('explored', sorted(explored))
    print('len explored', len(explored))
    
    for stop in explored:
        if stop not in TNW.all_stops():
            print(stop)
    
    assert sorted(explored) == sorted(stopdict.keys())
    


test_stops_exist()
test_lines_included()
test_feasible_distance()
test_connectedness()
    
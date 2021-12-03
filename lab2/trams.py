#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:18:50 2021

@author: adinahellstrom
"""
from graphs import *
import json
import math
import sys
sys.path.append('../lab1/')
import tramdata as td



"Objects of your own class can be included in dictionaries and arrays "
"like any other built-in data type in python. In this case, we want a"
"dictionary of objects of class TramStop and a dictionary of objects of class TramLine"



class TramNetwork(WeightedGraph):
    
    def __init__(self, lines, stops, times):
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times
        pass
    def all_lines(self):
        return list(self._linedict.keys())
    def all_stops(self):
        return list(self._stopdict.keys()) 
    def extreme_positions(self):
        pass
    def geo_distance(self, stops, a,b):
        D = td.distance_between_stops(stops, a, b)
        return D
    def line_stops(self, line):
        return self._linedict[line].__dict__['_stops']
    def remove_lines(self, lines):
        pass
    def stop_lines(self, a): #list of lines via the stop
        return 
    def transition_time(self, a,b):
        pass


class TramLine(TramNetwork):
    def __init__(self, num, stops):
        self._num = num
        self._stops = stops
    def get_number(self):
        return self._num
    def stops(self):
        return self._stops

"Its __init__() method needs the name as a required argument, whereas the"
"position and line list are optional. " # vad ska man göra med de som är optional?
class TramStops(TramLine): #Kanske behövs arv från TramNetwork här också?
    def __init__(self, name, lines=None, lat=None, lon=None):
        self._name = name
        self._lines = lines
        self._pos = (lat, lon)
    def add_line(self, line):
        self._lines.append(line)
    def get_lines(self):
        return self._lines
    def get_name(self):
        return self._name
    def get_position(self):
        return self._pos
    def set_position(self, lat, lon):
        self._pos = (lat, lon)

    
TRAM_FILE = '/Users/adinahellstrom/Documents/GitHub/DAT515/labb1/tramnetwork.json'
        
"It should return an object of class ``TramNetwork`."
def readTramNetwork(tramfile=TRAM_FILE):
    with open(TRAM_FILE) as f:
        data = json.load(f)
    linedict = data['lines']
    stopdict = data['stops']
    timedict = data['times']
    
    #print(linedict, stopdict, timedict)

    #namnet på hållplatsen är key, value: själva tramstop-objektet
    TramStops_dict = {}
    for stop in stopdict:
        lines_via_stop_list = []
        for line in linedict:
            if stop in linedict[line]:
                lines_via_stop_list.append(line)
        TramStop_obj = TramStops(stop, lines_via_stop_list, stopdict[stop]['lat'], stopdict[stop]['lon'])
        TramStops_dict[TramStop_obj.get_name()] = TramStop_obj
    
    #numret på linjen är key, value: själva tramline-objektet
    TramLine_dict = {}
    for line in linedict:
        TramLine_obj = TramLine(line, linedict[line])
        TramLine_dict[TramLine_obj.get_number()] = TramLine_obj
        
    
    # bygger hela TramNetwork-objektet
    TramNetwork_obj = TramNetwork(TramLine_dict, TramStops_dict, timedict)

    
    return TramNetwork_obj

G = readTramNetwork(tramfile=TRAM_FILE)

#print(G.__dict__)
print(G.all_lines())
print(G.all_stops())
print(len(G.all_stops()))
print('ETTANS: ', G.line_stops('1'))
print('FEMMANS: ', G.line_stops('5'))
print(type(G._stopdict))
print(G.geo_distance(G._stopdict, 'Brunnsparken','Svingeln'))




    
readTramNetwork(TRAM_FILE)


'''
    def demo():
        G = readTramNetwork()
        a, b = input('from,to ').split(',')
        graphs.view_shortest(G, a, b)

    if __name__ == '__main__':
        demo()
'''   
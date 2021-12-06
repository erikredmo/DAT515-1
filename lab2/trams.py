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


TRAM_FILE = '/Users/adinahellstrom/Documents/GitHub/DAT515/labb1/tramnetwork.json'


"Objects of your own class can be included in dictionaries and arrays "
"like any other built-in data type in python. In this case, we want a"
"dictionary of objects of class TramStop and a dictionary of objects of class TramLine"



class TramNetwork(WeightedGraph):
    
    def __init__(self, lines, stops, times):
        
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times
        
        edges = []
        
        for key in self._timedict.keys():
            for key2 in self._timedict[key].keys():
                if (key,key2) not in edges:
                    if (key2,key) not in edges:
                        edges.append((key,key2))
                        
                
        #print(edges)
    
        super().__init__(edges)
        for key in self._timedict.keys():
            for key2 in self._timedict[key].keys():
                super().set_weight(key,key2,self._timedict[key][key2])
                #print(key,key2,self._timedict[key][key2])
        
        
        
    def all_lines(self):
        return list(self._linedict.keys())
    def all_stops(self):
        return list(self._stopdict.keys()) 
    def geo_distance(self, stops, a,b):
        
        stopdict_new = {}
        for stop in self._stopdict:
            stopdict_new[stop] = {'lat' : self._stopdict[stop].get_position()[0], 'lon' : self._stopdict[stop].get_position()[1]}
        D = td.distance_between_stops(stopdict_new, a, b)
        return D
    def line_stops(self, line):
        return self._linedict[line].__dict__['_stops']
    def remove_lines(self, lines):
        self._linedict.pop(lines)
    def stop_lines(self, a): #list of lines via the stop
        return self._stopdict[a].get_lines()
    def transition_time(self, a,b):
        return self._timedict[a][b]


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

    


def demo():
    G = readTramNetwork(tramfile=TRAM_FILE)
    #print(G._weightlist)
    visualize(G)
    a, b = input('from,to ').split(',')
    view_shortest(G, a, b)
    
    
#    print(G.__dict__)
#    print(G.all_lines())
#    print(G.all_stops())
#    print(len(G.all_stops()))
#    print(G.geo_distance(G._stopdict, 'Brunnsparken','Östra Sjukhuset'))
#    print(G.geo_distance(G._stopdict, 'Brunnsparken','Lilla Bommen'))
#    print('ETTANS: ', G.line_stops('1'))
#    print('FEMMANS: ', G.line_stops('5'))
#    G.remove_lines('2')
#    print(G.all_lines())
#    print(G._stopdict['Sälöfjordsgatan'].get_name())
#    print(G.transition_time('Brunnsparken', 'Stenpiren'))
#    print(G.stop_lines('Stenpiren'))

if __name__ == '__main__':
    demo()
    
    
    
    
    
    
    

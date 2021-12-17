import json

# imports added in Lab3 version
import math
import os
from .graphs import WeightedGraph
from django.conf import settings
from .tramdata import distance_between_stops


# path changed from Lab2 version
# TODO: copy your json file from Lab 1 here
TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')


# TODO: use your lab 2 class definition, but add one method  
    

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
                        

    
        super().__init__(edges)
        for key in self._timedict.keys():
            for key2 in self._timedict[key].keys():
                super().set_weight(key,key2,self._timedict[key][key2])
        
        
        
    def all_lines(self):
        return list(self._linedict.keys())
    def all_stops(self):
        #return list(self._stopdict.keys()) # stop objects
        return self._stopdict.values() # lista på alla stop object
    
    def geo_distance(self, stops, a,b):
        
        stopdict_new = {}
        for stop in self._stopdict:
            stopdict_new[stop] = {'lat' : self._stopdict[stop].get_position()[0], 'lon' : self._stopdict[stop].get_position()[1]}
        D = distance_between_stops(stopdict_new, a, b)
        return D
    def line_stops(self, line):
        return self._linedict[line].__dict__['_stops']
    def remove_lines(self, lines):
        self._linedict.pop(lines)
    def stop_lines(self, a): 
        return self._stopdict[a].get_lines()
    def transition_time(self, a,b):
        return self._timedict[a][b]
    def extreme_positions(self):
        stops = self._stopdict.values() # stop objects
        minlon = float(min([s._pos[1] for s in stops]))
        minlat = float(min([s._pos[0] for s in stops]))
        maxlon = float(max([s._pos[1] for s in stops]))
        maxlat = float(max([s._pos[0] for s in stops]))
        
        return minlon, minlat, maxlon, maxlat


class TramLine(TramNetwork):
    def __init__(self, num, stops):
        self._num = num
        self._stops = stops
    def get_number(self):
        return self._num
    def stops(self):
        return self._stops

"Its __init__() method needs the name as a required argument, whereas the"
"position and line list are optional. "
class TramStops(TramLine):
    def __init__(self, name, lines=None, lat=None, lon=None):
        self._name = name
        self._lines = lines
        self._pos = (float(lat), float(lon))
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

    


#def readTramNetwork():
    # TODO: your own trams.readTramNetwork()
    "It should return an object of class ``TramNetwork`."
def readTramNetwork(tramfile=TRAM_FILE):
    with open(TRAM_FILE) as f:
        data = json.load(f)
    linedict = data['lines']
    stopdict = data['stops']
    timedict = data['times']

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


# Bonus task 1: take changes into account and show used tram lines

def specialize_stops_to_lines(network):
    # TODO: write this function as specified
    return network


def specialized_transition_time(spec_network, a, b, changetime=10):
    # TODO: write this function as specified
    return changetime


def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
    # TODO: write this function as specified
    return changedistance



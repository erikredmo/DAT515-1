#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:18:50 2021

@author: adinahellstrom
"""


class TramNetwork:
    
    def __init__(self, lines, stops, times):
        self.lines = lines
        self.stops = stops
        self.times = times
        pass
    def all_lines(self):
        pass
    def all_stops(self):
        pass
    def extreme_positions(self):
        pass
    def geo_distance(self, a,b):
        pass
    def line_stops(self, line):
        pass
    def remove_lines(self, lines):
        pass
    def stop_lines(self, a):
        pass
    def transition_time(self, a,b):
        pass
    
class TramLine(TramNetwork):
    def __init__(self, num, stops):
        self.num = num
        self.stops = stops
    def get_number(self):
        pass
    def stops(self):
        pass
    
class TramStops(TramLine):
    def __init__(self, name, lines, lat, lon):
        self.name = name
        self.lines = lines
        self.lat = lat
        self.lon = lon
    def add_line(self, line):
        pass
    def get_lines(self):
        pass
    def get_name(self):
        pass
    def get_position(self):
        pass
    def set_position(self, lat,lon):
        pass
    
def readTramNetwork(file=filename):
    pass
    
# in trams.py
readTramNetwork(file='tramnetwork.json')
        

        
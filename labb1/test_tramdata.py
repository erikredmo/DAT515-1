import unittest
from tramdata import *

TRAM_FILE = 'tramnetwork.json'

import itertools

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    # add your own tests here
    def test_lines_included(self):
        f = open('data/tramlines.txt')
        lines = f.readlines()
        f.close()
        lines_list = []
        
        for line in lines:
            lines_list.append(line.strip('\n'))
            
        line_numbers = []
        
        for i in range(len(lines_list)-1):
            if i == 0:
                line_numbers.append(lines_list[i][:-1])
            elif lines_list[i] == '':
                line_numbers.append(lines_list[i+1][:-1])
        
        for element in line_numbers:
            self.assertIn(element, list(self.linedict.keys()), msg = element + ' not in linedict')
        
                          
    def test_stops_exist_in_file(self):
        
        f = open('data/tramlines.txt')
        tramline_blocks = f.read().split('\n\n')
        f.close()
        big_stops_list = []
        
        for element in tramline_blocks[:-1]:
            lines = element.split('\n')
            line_list = []
            for line in lines[1:]:
                line_list.append(line[:-5].strip())
            big_stops_list.append(line_list)
    
        list_of_stoplists = list(self.linedict.values())
        big_stops_list2 = []
        for element in list_of_stoplists:
            big_stops_list2.append(element)
      
        self.assertEqual(big_stops_list, big_stops_list2)


    def test_feasible_distance(self):
        
        all_combinations = list(itertools.product(list(self.stopdict.keys()), list(self.stopdict.keys())))
        D_list = []
        for comb in all_combinations:
            D_list.append(int(distance_between_stops(self.stopdict, comb[0], comb[1])))
        
        D_max = max(D_list)
        self.assertLess(D_max, 20000, msg=None)

    def test_same_time(self):

        for line_nr in list(self.linedict.keys()):
            all_combinations = list(itertools.product(self.linedict[line_nr], self.linedict[line_nr]))
            for comb in all_combinations:
                time1 = time_between_stops(self.linedict, self.timedict, line_nr, comb[0], comb[1])
                time2 = time_between_stops(self.linedict, self.timedict, line_nr, comb[1], comb[0])
                
                
                self.assertEqual(time1, time2, msg=None)



if __name__ == '__main__':
    unittest.main()


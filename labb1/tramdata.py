# Lab 1
import json

def build_tram_stops(jsonobject):
    with open(jsonobject) as json_file:
        data = json.load(json_file)
    tram_stops = {}
    
    for i in range(len(list(data.values()))):
        position_dict = {}
        position_dict.setdefault('lat', list(data.values())[i]['position'][0])
        position_dict.setdefault('lon', list(data.values())[i]['position'][1])
        tram_stops.setdefault(list(data.keys())[i], position_dict)

    return tram_stops


def build_tram_lines(txtfilename):
    f = open(txtfilename)
    lines = f.readlines()
    f.close()
    lines_list = []
    for i in lines:
        lines_list.append(i.strip('\n'))

    line_numbers = {}
    current_line_stops= []
    current_line_times = []
    time_dict = {}

    for i in range(len(lines_list)):
        if i == 0:
            line_number = lines_list[i][:-1]
            current_line_stops.append(lines_list[i+1][:-5].strip())   # ???
            current_line_times.append(lines_list[i+1][-2:])
        elif i == len(lines_list)-1:
            line_numbers.setdefault(line_number, current_line_stops[:-1])
        elif lines_list[i] == '':
            line_numbers.setdefault(line_number, current_line_stops[:-1])
            line_number = lines_list[i+1][:-1]
            
            
            # time_dict
            for i in range(len(current_line_stops)+1):
                if current_line_stops[i+1] == '':
                    break
                if current_line_stops[i] in time_dict:
                    if current_line_stops[i+1] in time_dict[current_line_stops[i]]:
                        continue
                    elif current_line_stops[i+1] in time_dict:
                        if current_line_stops[i] in time_dict[current_line_stops[i+1]]:
                            continue                    
                        else:
                            time_dict[current_line_stops[i+1]].update({current_line_stops[i]:(int(current_line_times[i+1])-int(current_line_times[i]))})
                        
                    
                else:
                    time_dict[current_line_stops[i]] = {current_line_stops[i+1]:(int(current_line_times[i+1])-int(current_line_times[i]))}
                    
                    
            current_line_stops = []
            current_line_times = []
        else:
            next_stop = lines_list[i+1][:-5].strip()
            current_time = lines_list[i+1][-2:]
            current_line_stops.append(next_stop)
            current_line_times.append(current_time)
          
    return line_numbers, time_dict
    

def build_tram_network(jsonfile, txtfile):
    
    data = {'stops': build_tram_stops(jsonfile), 'lines': build_tram_lines(txtfile)[0], 'times': build_tram_lines(txtfile)[1]}
    
    
    with open('tramnetwork.json', 'w') as f:
        json.dump(data, f)
    
        
  
######## QUERY FUNCTIONS ########

def lines_via_stop(tramdict, stop):
    
    lines_list = []
    lines_dict = tramdict['lines']
    
    lines = list(lines_dict.keys()) # 1, 2, 3 osv alla linjer
    stops_list = list(lines_dict.values()) # lista med listor med hållplatser
    
    
    for stops in stops_list:
        for station in stops:
            if station == stop:
                lines_list.append(int(lines[stops_list.index(stops)]))
    
    sorted_lines = [str(element) for element in sorted(lines_list)]
    
    return sorted_lines



def lines_between_stops(tramdict, stop1, stop2):
    lines_between_stops = []
    
    lines_dict = tramdict['lines']
    lines = list(lines_dict.keys()) # 1, 2, 3 osv alla linjer
    stops_list = list(lines_dict.values()) # lista med listor med hållplatser
    
    
    for stops in stops_list:
        if stop1 in stops and stop2 in stops:
            lines_between_stops.append(int(lines[stops_list.index(stops)]))
        
    sorted_between_stops = [str(element) for element in sorted(lines_between_stops)]
    
    return sorted_between_stops



def where_is_connection(stop1, stop2, time_dict):
    if stop1 in time_dict:
        if stop2 in time_dict[stop1]:
            return stop1, stop2 # stop1 är key i time_dict, stop2 är value till den keyn
        elif stop2 in time_dict:
            if stop1 in time_dict[stop2]:
                return stop2, stop1 #stop2 är key i time_dict, stop1 är value till den keyn
    else:
        return stop2, stop1

def time_between_stops(lines_dict, time_dict, line, stop1, stop2):
    line_list = lines_dict[line]
    stop1_to_stop2 = []
    index1 = 0
    index2 = 0
    if stop1 not in line_list or stop2 not in line_list:
        print('stops are not along the same line')
    
    index1 = line_list.index(stop1)
    index2 = line_list.index(stop2)

    if index1 < index2:
        stop1_to_stop2 = line_list[index1:index2+1]
    else:
        stop1_to_stop2 = line_list[index2:index1+1]
    
    time_sum = 0

    tuple_stops = where_is_connection(stop1, stop2, time_dict)
    
    for i in range(len(stop1_to_stop2)-1):
        
        
        tuple_stops = where_is_connection(stop1_to_stop2[i], stop1_to_stop2[i+1], time_dict)
        
        #if tuple_stops[0] is None or tuple_stops[1] is None:
        NoneType = type(None)
        if not isinstance(tuple_stops, NoneType):
        
            time_sum += time_dict[tuple_stops[0]][tuple_stops[1]]

    
    return time_sum


import math

def lonlat_to_rad(value):
    return value * math.pi/180

def distance_between_stops(stop_dict, stop1, stop2):

    
    delta_lat = abs(lonlat_to_rad(float(stop_dict[stop1]['lat'])) - lonlat_to_rad(float(stop_dict[stop2]['lat'])))
    delta_lon = abs(lonlat_to_rad(float(stop_dict[stop1]['lon'])) - lonlat_to_rad(float(stop_dict[stop2]['lon'])))
    mean_lat = (lonlat_to_rad(float(stop_dict[stop1]['lat'])) + lonlat_to_rad(float(stop_dict[stop2]['lat'])) )/ 2
    
    
    R = 6371009
    
    D = R * math.sqrt((delta_lat)**2 + (math.cos(mean_lat)*delta_lon)**2)
    
    return D



def dialogue(jsonfile):

    
    with open(jsonfile) as json_file:
        data = json.load(json_file)
    
    while True:
        user_input = input('> ')
        if user_input == 'quit':
            break
        else:
            if answer_query(data, user_input) == False:
                print('Sorry, try again.')
                dialogue()
            else:
                print(answer_query(data, user_input))
                return answer_query(data, user_input)
    

def answer_query(tramdict, query):
    query_str_list = query.split()

    # Via
    if query_str_list[0] == 'via':
        if len(query_str_list) > 2:
            try: 
                prel_stop = ' '.join(query_str_list[1:])
                prel_lines = lines_via_stop(tramdict, prel_stop)
                return prel_lines
            except:
                return False
        else:
            try:
                prel_stop = query_str_list[1]
                prel_lines = lines_via_stop(tramdict, prel_stop)
                return prel_lines
            except:
                print('Unknown error')
    
    # Line between
    elif query_str_list[0] == 'between':
        try: 
            stop1 = ' '.join(query_str_list[1:query_str_list.index('and')])
            stop2 = ' '.join(query_str_list[query_str_list.index('and')+1:])
            return lines_between_stops(tramdict, stop1, stop2)
        except:
            return False

    # Time between
    elif query_str_list[0] == 'time':
        try:
            line = ''.join(query_str_list[query_str_list.index('with')+1:query_str_list.index('from')])
            stop1 = ' '.join(query_str_list[query_str_list.index('from')+1:query_str_list.index('to')])
            stop2 = ' '.join(query_str_list[query_str_list.index('to')+1:])
            return time_between_stops(tramdict['lines'], tramdict['times'], line, stop1, stop2)
        except:
            return False
        

        
        
def dialogue(jsonfile):
    with open(jsonfile) as json_file:
        data = json.load(json_file)

    while True:
        user_input = input('> ')
        if user_input == 'quit':
            break
        else:
            if answer_query(data, user_input) == False:
                print('Sorry, try again.')
            else:
                print(answer_query(data, user_input))
    

def answer_query(tramdict, query):
    query_str_list = query.split()
    linedict = tramdict['lines']
    timedict = tramdict['times']
    stopdict = tramdict['stops']

    # Via
    if query_str_list[0] == 'via':
        try: 
            stop = ' '.join(query_str_list[query_str_list.index('via')+1:])
            if stop not in tramdict['stops']:
                print('Unknown argument')
                return False
            else:
                return lines_via_stop(tramdict, stop)
        except:
            return False
    
    # Line between
    elif query_str_list[0] == 'between':
        try: 
            stop1 = ' '.join(query_str_list[1:query_str_list.index('and')])
            stop2 = ' '.join(query_str_list[query_str_list.index('and')+1:])
            if stop1 not in tramdict['stops'] or stop2 not in tramdict['stops']:
                print('Unknown arguments')
                return False
            else:
                return lines_between_stops(tramdict, stop1, stop2)
        except:
            return False

    # Time between
    elif query_str_list[0] == 'time':
        try:
            line = ''.join(query_str_list[query_str_list.index('with')+1:query_str_list.index('from')])
            stop1 = ' '.join(query_str_list[query_str_list.index('from')+1:query_str_list.index('to')])
            stop2 = ' '.join(query_str_list[query_str_list.index('to')+1:])
            if stop1 not in tramdict['stops'] or stop2 not in tramdict['stops']:
                print('Unknown arguments')
                return False
            elif line not in tramdict['lines']:
                print('Unknown arguments')
                return False
            else: 
                return time_between_stops(linedict, timedict, line, stop1, stop2)
        except:
            return False

    # Distance between
    elif query_str_list[0] == 'distance':
        try:
            stop1 = ' '.join(query_str_list[query_str_list.index('from')+1:query_str_list.index('to')])
            stop2 = ' '.join(query_str_list[query_str_list.index('to')+1:])
            if stop1 not in tramdict['stops'] or stop2 not in tramdict['stops']:
                print('Unknown arguments')
                return False
            else:
                return distance_between_stops(stopdict, stop1, stop2)
        except:
            return False


################ MAIN ###############
import sys

if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network('data/tramstops.json', 'data/tramlines.txt')
    else:
        dialogue('tramnetwork.json')
        
    

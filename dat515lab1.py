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

    lines_2 = []
    for i in lines:
        lines_2.append(i.strip('\n'))
    lines_2.insert(0, '')
    del lines_2[-1]
    line_numbers = {}
    current_line = []
    final_line_list = []
#    print(lines_2)

    for i in range(len(lines_2)):
        old_line_number = 0
        if lines_2[i] == '':
            line_number = lines_2[i+1][:-1]
            line_numbers[old_line_number] = current_line[2:]
            old_line_number = line_number
            print(line_numbers)
 #           line_number = lines_2[i+1][:-1]
 #           print(str(int(line_number)))
            current_line = []
        current_line.append(lines_2[i][:-5].strip())
 #       print(line_number)
 #       print(current_line)
 #       print(line_numbers)
 #       print(current_line)
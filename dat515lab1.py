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

    
    
    line_numbers = {}
    current_line = []
    for i in range(len(lines_2)):
        if i == 0:
            line_number = lines_2[i]
            current_line.append(lines_2[i][:-5].strip())
        elif i == len(lines_2)-1:
            line_numbers.setdefault(line_number, current_line[1:])
#            break
        elif lines_2[i] == '':
            line_numbers.setdefault(line_number, current_line[1:])
            line_number = lines_2[i+1]
            current_line = []
        
        else:
            current_line.append(lines_2[i][:-5].strip())

            
    return line_numbers
    
print(build_tram_lines('/Users/erikredmo/Documents/GitHub/chalmers-advanced-python/labs/data/tramlines.txt'))


#HEJ HEJ /ADINA

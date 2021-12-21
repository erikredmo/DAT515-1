# baseline tram visualization for Lab 3, modified to work with Django

from .trams import readTramNetwork
from .trams import w_time_to_distance
from .graphs import dijkstra
from .graphs import *
import graphviz
import json
import os
from django.conf import settings

# to be defined in Bonus task 1, but already included as mock-up
from .trams import specialize_stops_to_lines, specialized_geo_distance, specialized_transition_time

SHORTEST_PATH_SVG = os.path.join(settings.BASE_DIR,
                        'tram/templates/tram/images/shortest_path.svg')


# assign colors to lines, indexed by line number; not quite accurate
gbg_linecolors = {
    1: 'gray', 2: 'yellow', 3: 'blue', 4: 'green', 5: 'red',
    6: 'orange', 7: 'brown', 8: 'purple', 9: 'blue',
    10: 'lightgreen', 11: 'black', 13: 'pink'}


def scaled_position(network):

    # compute the scale of the map
    minlat, minlon, maxlat, maxlon = network.extreme_positions()
    size_x = maxlon - minlon
    scalefactor = len(network)/4  # heuristic
    x_factor = scalefactor/size_x
    size_y = maxlat - minlat
    y_factor = scalefactor/size_y
    
    return lambda xy: (x_factor*(xy[0]-minlon), y_factor*(xy[1]-minlat))

# Bonus task 2: redefine this so that it returns the actual traffic information

from bs4 import BeautifulSoup
import requests

def stop_url_list(network):

    source = requests.get('https://www.vasttrafik.se/reseplanering/hallplatslista/').text
    soup = BeautifulSoup(source, 'html.parser')
    
    gids = []
    stops_added = []
    for item in soup.find_all('li', class_="mb-1"):
        item_text = item.a.text.split()
        if type(item_text[0][0]) == int:
            continue
        for i in range(len(item_text)):
            item_text[i] = item_text[i].strip(',')
        
        if len(item_text) > 4:
            new_stop = ''
            for i in range(len(item_text)-3):
                new_stop = new_stop + item_text[i] + ' '
            item_text[0] = new_stop[:-1]
            item_text = item_text[:1] + item_text[-3:]
        
        for stop in network._stopdict.keys():
            #göteborg adderas före mölndal pga G kmr före M
            if stop in item_text and ('Göteborg' in item_text or 'Mölndal' in item_text) and stop not in stops_added:
                stops_added.append(stop)
                gids.append((stop, item.find('a').get('href')[-17:-1]))
        
        
        urls = []
        url_beginning = 'https://avgangstavla.vasttrafik.se/?source=vasttrafikse-stopareadetailspage&stopAreaGid='
        for gid in gids:
            url_full = url_beginning + gid[1]
            urls.append((gid[0], url_full))
        
    return urls



def stop_url(stop, urls):
    for url in urls:
        if url[0] == stop:
            print(url[1])
            return url[1]

    
#    google_url = 'https://www.google.com/search'
#    attrs = urllib.parse.urlencode({'q': 'Gothenburg ' + stop.get_name()})
#    return google_url + '?' + attrs


# You don't probably need to change this

def network_graphviz(network, outfile, colors=None, positions=scaled_position):
    dot = graphviz.Graph(engine='fdp', graph_attr={'size': '12,12'})
    
    url_list = stop_url_list(network)
    print(url_list)

    for stop in network.all_stops(): # går igenom alla stop objects
        
        y, x = stop.get_position() # go to a stop object
        if positions:
            x, y = positions(network)((x, y)) 
        pos_x, pos_y = str(x), str(y)
        
        if colors:
            col = colors(stop.get_name()) # set this to white to create gbg_tramnet.svg
        else:
            col = 'white'
            
        dot.node(stop.get_name(), label=stop.get_name(), shape='rectangle', pos=pos_x + ',' + pos_y,
            fontsize='8pt', width='0.4', height='0.05',
            URL=stop_url(stop.get_name(), url_list),
            fillcolor=col, style='filled')
        
    for line in network.all_lines():
        stops = network.line_stops(line)
        for i in range(len(stops)-1):
            dot.edge(stops[i], stops[i+1],
                         color=gbg_linecolors[int(line)], penwidth=str(2))
            

    dot.format = 'svg'
    s = dot.pipe().decode('utf-8')
    with open(outfile, 'w') as file:
        file.write(s)
        

    

def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code
    network_time = readTramNetwork()
    network_distance = readTramNetwork()
    w_time_to_distance(network_distance)
    
    print(type(network_time.edges()[0][0][0]))
    

    # BONUS PART 1
    vertices = []
    for stop in network_time._stopdict.values(): #tramstop-objekt
        lines = stop.get_lines() 
        for line in lines:
            vertices.append((stop.get_name(), line))
    
    edgelist = []
    for edge in network_time.edges():
        for line in network_time._stopdict[edge[0]].get_lines():
            if line in network_time._stopdict[edge[1]].get_lines():
                edgelist.append(((edge[0], line), (edge[1], line)))
       
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            if vertices[i][0] == vertices[j][0] and vertices[i][1] != vertices[j][1]:
                edgelist.append(((vertices[i]), vertices[j]))
            
    extra_graph_time = WeightedGraph(edgelist)
    extra_graph_distance = WeightedGraph(edgelist)
    for i in range(len(edgelist)):
        if edgelist[i][0][0] == edgelist[i][1][0] and edgelist[i][0][1] != edgelist[i][1][1]:
            # add 20 meters resp 10 minutes
            extra_graph_time.set_weight(edgelist[i][0], edgelist[i][1], 10)
            extra_graph_distance.set_weight(edgelist[i][0], edgelist[i][1], 20)
        
        else:
            extra_graph_time.set_weight(edgelist[i][0], edgelist[i][1], network_time.get_weight(edgelist[i][0][0], edgelist[i][1][0]))
            extra_graph_distance.set_weight(edgelist[i][0], edgelist[i][1], network_distance.get_weight(edgelist[i][0][0], edgelist[i][1][0]))
  
    

    # TODO: replace this mock-up with actual computation using dijkstra
    quickest_path = 'The quickest route from ' + dep + ' to ' + dest
    shortest_path = 'The shortest route from ' + dep + ' to ' + dest


    
    #TIME NETWORK WITH BONUS 1
    quickest_path = view_shortest(extra_graph_time, dep, dest)
    
    #DISTANCE NETWORK WITH BONUS 1
    shortest_path = view_shortest(extra_graph_distance, dep, dest)

    
    # COLORS
    # TODO: run this with the shortest-path colors to update the svg image
    #green for stops on the shortest path
    #orange for stops on quickest path
    #cyan for stops that are on both paths
    def colors(stop):
        #print(stop)
#        print(shortest_path)
        color = 'white'
        if stop in shortest_path[0]:
            color = 'orange'
        
        if stop in quickest_path[0]:
            color = 'green'
            
        if stop in quickest_path[0] and stop in shortest_path[0]:
            color = 'cyan'
        return color
    

    network_graphviz(network_time, SHORTEST_PATH_SVG, colors=colors)
    
    return quickest_path[1], shortest_path[1]


# baseline tram visualization for Lab 3, modified to work with Django

from .trams import readTramNetwork
from .trams import w_time_to_distance
from .graphs import dijkstra
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
import urllib.parse
def stop_url(stop):
    google_url = 'https://www.google.com/search'
    attrs = urllib.parse.urlencode({'q': 'Gothenburg ' + stop.get_name()})
    return google_url + '?' + attrs


# You don't probably need to change this

def network_graphviz(network, outfile, colors=None, positions=scaled_position):
    dot = graphviz.Graph(engine='fdp', graph_attr={'size': '12,12'})

    for stop in network.all_stops(): # går igenom alla stop objects
        
        x, y = stop.get_position() # go to a stop object
        if positions:
            x, y = positions(network)((x, y))
        pos_x, pos_y = str(x), str(y)
        
        if colors:
            col = colors(stop.get_name()) # set this to white to create gbg_tramnet.svg
        else:
            col = 'white'
            
        dot.node(stop.get_name(), label=stop.get_name(), shape='rectangle', pos=pos_x + ',' + pos_y +'!',
            fontsize='8pt', width='0.4', height='0.05',
            URL=stop_url(stop),
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


'''
from bs4 import BeautifulSoup
import urllib.request

def extracting_gids():
    with open('hallplatslista.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    
    data = soup.find_all('li', { 'class':'mb-1'})
    numbers = [d.text for d in data]
'''
    

def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code
    network_time = readTramNetwork()
    network_distance = readTramNetwork()
    w_time_to_distance(network_distance)
    
    
    # BONUS PART 1
    vertices = []
    for stop in network_time._stopdict:
        lines = stop.get_lines()
        for line in lines:
            vertices.append((stop, line))
    
    edgelist = []
    for edge in network_time.edges():
        if edge[0] in edge[0].get_lines() and edge[1] in edge[1].get_lines():
            edgelist.append(())
        
    
    extra_graph = WeightedGraph(edgelist)
    
    
    
    

    
    print(network_time.get_weight('Chalmers', 'Kapellplatsen'))
    print(network_distance.get_weight('Chalmers', 'Kapellplatsen'))
    

    # TODO: replace this mock-up with actual computation using dijkstra
    quickest_path = 'The quickest route from ' + dep + ' to ' + dest
    shortest_path = 'The shortest route from ' + dep + ' to ' + dest

    # TODO: run this with the shortest-path colors to update the svg image
    
    #green for stops on the shortest path
    #orange for stops on quickest path
    #cyan for stops that are on both paths
    
    #TIME NETWORK
    
    quickest_path = dijkstra(network_time, dep)[dest]
    quickest_path.append(dest)
    
    
    #DISTANCE NETWORK
    shortest_path = dijkstra(network_distance, dep)[dest]
    shortest_path.append(dest)
    
    
    # COLORS
    
    def colors(stop):
        color = 'white'
        if stop in shortest_path:
            color = 'orange'
        
        if stop in quickest_path:
            color = 'green'
            
        if stop in quickest_path and stop in shortest_path:
            color = 'cyan'
        return color
    
    
    network_graphviz(network_time, SHORTEST_PATH_SVG, colors=colors)
    
    #parameter colors in network_graphviz should be a function that we create which returns the correct color for each stop
    
    return quickest_path, shortest_path



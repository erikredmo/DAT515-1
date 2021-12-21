# TODO: mock-up to be replaced by your file from Lab 2

class Graph:
    def __init__(self, edgelist=None, start=None, values=None, directed=False):
        self._edgelist = edgelist
        self._adjlist = Graph.edges2adjacency(edgelist)
        self._redadjlist = Graph.rededges2adjacency(edgelist)
        if values is None:
            values = {}
        self._valuelist = values #values of nodes
        self._isdirected = directed # False => undirected
        


# Gör om edges till adjacency list där varje nod är key och dess values dess kopplingar
    def rededges2adjacency(edges):
        adj = {}
        for (src,dst) in edges:
            if src in adj:
                if dst not in adj:
                    adj[dst] = [src]
                if dst not in adj[src]:
                    adj[src].append(dst)
                if src not in adj[dst]:
                    adj[dst].append(src)
                else:
                    continue
            elif dst in adj:
                if src not in adj:
                    adj[src] = [dst]
                if src not in adj[dst]:
                    adj[dst].append(src)
                if dst not in adj[src]:
                    adj[src].append(dst)
            else:
                adj[src] = [dst]
                adj[dst] = [src]

        #return dict(adj.items())
        return dict(sorted(adj.items()))
        


# Gör om edges till adjacency list utan redundans
    def edges2adjacency(edges):
        adj = {}
        for (src,dst) in edges:
            if src in adj:
                if dst in adj[src]:
                    continue
                elif dst in adj:
                    if src in adj[dst]:
                        continue
                    else:
                        adj[dst].append(src)
                else:
                    adj[src].append(dst)
            elif dst in adj:
                if src in adj[dst]:
                    continue
                else: 
                    adj[dst].append(src)
            else:
                adj[src] = [dst]
                
        return adj
    
    
# Returnerar lista med grannar till nod v
    def neighbours(self, v):
        return self._redadjlist[v]
# Returnerar lista av samtliga noder
    def vertices(self):
        return self._redadjlist.keys()
# Returnerar kopplingar (edges)
    def edges(self):
        return self._edgelist
# Returnerar antalet noder
    def __len__(self):
        return len(self._redadjlist.keys())
# Lägg till en nod    
    def add_vertex(self, v):
        self._adjlist.setdefault(v, [])
        self._redadjlist.setdefault(v, [])
# Lägg till en koppling (edge)
    def add_edge(self, v1, v2):
        # I _edgelist
        if (v1,v2) not in self._edgelist:
            if (v2,v1) not in self._edgelist:
                self._edgelist.append((v1,v2))
        # I _adjlist
        if v1 not in self._adjlist:
            if v2 in self._adjlist:
                if v1 not in self._adjlist[v2]:
                    self._adjlist[v2].append(v1)
            else:
                self._adjlist[v1] = [v2]
        elif v2 not in self._adjlist[v1]:
            self._adjlist[v1].append(v2)
        # I _redadjlist
        if v1 not in self._redadjlist:
            self._redadjlist.setdefault(v1, [v2])
        elif v2 not in self._redadjlist[v1]:
            self._redadjlist[v1].append(v2)
        if v2 not in self._redadjlist:
            self._redadjlist.setdefault(v2, [v1])
        elif v1 not in self._redadjlist[v2]:
            self._redadjlist[v2].append(v1)
# Ta bort en nod (vertex)
    def remove_vertex(self, v):
        # I _edgelist
        for edge in self._edgelist:
            if v in edge:
                self._edgelist.remove(edge)
        # I _adjlist
        if v in self._adjlist:
            del self._adjlist[v]
        for node in self._adjlist:
            if v in node:
                self._adjlist[node].remove(v)
        # I _redadjlist
        if v in self._redadjlist:
            del self._adjlist[v]
        for node in self._redadjlist:
            if v in node:
                self._redadjlist[node].remove(v)
# Tar bort edge
    def remove_edge(self, v1, v2):
        # I _edgelist
        for edge in self._edgelist:
            if edge == (v1,v2) or edge == (v2,v1):
                self._edgelist.remove(edge)
        # I _adjlist
        for node in self._adjlist:
            if node == v1:
                if v2 in self._adjlist[node]:
                    self._adjlist[node].remove(v2)
            if node == v2:
                if v1 in self._adjlist[node]:
                    self._adjlist[node].remove(v1)
        # I _redadjlist
        for node in self._redadjlist:
            if node == v1:
                if v2 in self._redadjlist[node]:
                    self.redadjlist[node].remove(v2)
            if node == v2:
                if v1 in self._redadjlist[node]:
                    self._redadjlist[node].remove(v1)
# Getter för edgelist
    def get_edgelist(self):
        return self._edgelist
# Getter för adjlist
    def get_adjlist(self):
        return self._adjlist
# Getter för redadjlist
    def get_redadjlist(self):
        return self._redadjlist
# Getter för nodens namn
    def get_vertex_value(self, v):
        index = list(self._valuelist.keys()).index(v)
        return list(self._adjlist.keys())[index]
# Setter för nodens namn?
    def set_vertex_value(self, v, x):
        self._valuelist[v] = x 


class WeightedGraph(Graph):
    def __init__(self, edgelist):
        super().__init__(edgelist) 
        self._weightlist = {}
# Returnerar vikt för edge
    def get_weight(self, v1, v2):
        if (v1,v2) in self._weightlist:
            return self._weightlist[(v1,v2)]
        elif (v2,v1) in self._weightlist:
            return self._weightlist[(v2,v1)]
# Gör edge till key i weightlist och ger den värdet weight
    def set_weight(self, v1, v2, w):
        self._weightlist[(v1,v2)] = w
        self._weightlist[(v2,v1)] = w

def dijkstra(graph, source, cost=lambda u,v: 1):
    visited = []
    shortest_from_source_dict = {}
    shortest_to_show_dict = {}
    path = {}
    for vertex in graph.vertices():
        shortest_from_source_dict[vertex] = float('inf')
        path[vertex] = []
        if vertex[0] == source:
            shortest_from_source_dict[vertex] = 0

    def dijkstraloop(source):
        should_do_loop = True
        if len(visited) == 0:
            for stop in graph._redadjlist:
                if stop[0] == source and stop not in visited:
                    source = stop
                
        for neighbour in graph._redadjlist[source]:
            if neighbour not in visited:
                if type(graph) == WeightedGraph:
                    neighbour_cost = shortest_from_source_dict[source] + graph.get_weight(source, neighbour)
                else:
                    neighbour_cost = shortest_from_source_dict[source] + cost(source, neighbour)
                if neighbour_cost < shortest_from_source_dict[neighbour]:
                    shortest_from_source_dict[neighbour] = neighbour_cost
                    prev_path = path[source]
                    path[neighbour] = []
                    if prev_path == []:
                        path[neighbour].append(source)
                    elif prev_path == path[neighbour]:
                        #print(prev_path)
                        path[neighbour].append(source)
                    else:
                        for prev in prev_path:
                            path[neighbour].append(prev)
                        path[neighbour].append(source)
                else:
                    continue
            else:
                continue

        visited.append(source)
 
        if len(visited) == len(graph.vertices()):
            should_do_loop = False
            return path, shortest_to_show_dict
        else:
            shortest_to_show_dict.update({source: shortest_from_source_dict.pop(source, None)})
            shortest_from_source_dict.pop(source, None)
            min_value_index = list(shortest_from_source_dict.values()).index(min(shortest_from_source_dict.values()))
            min_from_source = list(shortest_from_source_dict.keys())[min_value_index]
            if should_do_loop == True:
                return dijkstraloop(min_from_source)
 
    return dijkstraloop(source)


def view_shortest(graph, source, target):
    dijk = dijkstra(graph, source)
    path = dijk[0]
    cost = dijk[1]
    
    for stop in path.keys():
        if stop[0] == target:
            path_to_change = path[stop]
    path_to_show = []
    for station in path_to_change:
        if len(path_to_show) == 0:
            path_to_show.append('Go with tram number: ' + station[1])
            path_to_show.append(station[0])
        elif station[0] in path_to_show:
            path_to_show.append(' Change to tram number: ' + station[1])
            path_to_show.append(station[0])
        else: 
            path_to_show.append(station[0])
    if path_to_show[-1] != target:
        path_to_show.append(target)
    if type(cost[path_to_change[-1]]) == int:
        path_to_show.append(str(round(cost[path_to_change[-1]])))
        path_to_show.append(' min')
        
    else:
        path_to_show.append(str(round(cost[path_to_change[-1]])/1000))
        path_to_show.append(' km')
    
    return path_to_show, ', '.join(path_to_show)

import graphviz

def visualize(graph, view='dot', name='mygraph', nodecolors=None, view_shortest=False):
    dot = graphviz.Graph(engine='dot')
    if view_shortest == True:
        for v in graph.vertices():
            if str(v) in nodecolors:
                dot.node(str(v), color=nodecolors[str(v)])
            else:
                dot.node(str(v))
    elif view_shortest == False:
        for v in graph.vertices():
            dot.node(str(v))
    for (a,b) in graph.edges():
        dot.edge(str(a),str(b))
    dot.render('mygraph.gv', view=True)
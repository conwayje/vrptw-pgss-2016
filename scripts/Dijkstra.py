from ImportCustomers import import_customers
#this doesn't work yet
def create_graph(customers):
    g = {}
    for c in customers:
        print('graphing')
        g[c] = {}
        for d in customers:
            g[c][d] = d.distance_to_customer(c)
    return g
    
def get_distance(self, vertex):
    return ((vertex.y - self.y)**2 + (vertex.x - self.x)**2)**0.5
    
def shortest_path(graph, source, target):
    d,p = djikstra(source, target, graph)
    path = []
    while 1:
        path.append(target)
        if target == source: break
        #target = p[target]
    path.reverse()
    return path
    
#def djikstra(source, end, graph):
#    d = {}
#    p = {}
#    q = {}
#    q[source] = 0
#    for v in graph:
#        d[v] = float('inf')
#    d[source] = 0
#    
#    for w in graph[v]:
#        print("doing djikstra")
#        l = graph[v][w]
#        if w in d: 
#            if l < d[w]: #distance is less than old distance
##                print("idk what to do here")
##            elif w not in q or l < q[w]: 
##                q[w] = l 
#            p[w] = v #add previous vertex as predecessor in the path
#    
#    return(d,p)

def nearest_neighbors(customers, source, end):
    graph = create_graph(customers)
    p = {}
    d = {}
    for cust in graph:
        d[cust] = float('inf')
    d[source] = 0

    dist = float('inf')
    for cust in graph[source]:
        d[cust] = graph[source][cust]
        if d[cust] < dist:
            dist = d[cust]
            p[cust] = source
        
    print p
    path = [source]
    for cust in p:
        while not(cust == end and len(path) == len(customers)):
            path.append(p[cust])
        path.append(end)
    print path

def do_dijkstra(customers, source, end):
    nearest_neighbors(customers, source, end)

custs = import_customers("C201.txt")
custs = custs[1:15]
do_dijkstra(custs, custs[1], custs[13])


#def get_adjacent_node(source, vertices):
#    node = None
#    distance = 200 #arbitrary value
#    for vertex in vertices:
#        new_distance = vertex.get_distance(source)
#        if new_distance <= distance:
#            distance = new_distance
#    return node, new_distance
#    
#def get_closest_node(source, vertices):
#    node = None
#    vertices = sorted(vertices, key=lambda vertex: vertex.get_distance(source))
#    node = vertices[0]
#    return node
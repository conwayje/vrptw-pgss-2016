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

# @TODO -- should probably refer to DistanceMatrix
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

# @TODO -- please base this on the 
custs = import_customers("C201.txt")
custs = custs[1:15]
do_dijkstra(custs, custs[1], custs[13])
from ImportCustomers import import_customers
from Distances import Distances
#this doesn't work yet

def create_matrix(customers):
    return Distances.calculate_matrix(customers)
    
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
    
#def shortest_path(graph, source, target):
#    d,p = djikstra(source, target, graph)
#    path = []
#    while 1:
#        path.append(target)
#        if target == source: break
#        #target = p[target]
#    path.reverse()
#    return path
    
#def shortest_paths(source, end, matrix):
#    p = {} #predecessors
#    d = {}
#    path = []
#    path.append(source)
#    while len(path) < len(matrix):
#        path.append(get_closest(source, matrix, path, end))
#        source  = get_closest(source, matrix, path, end)
#    path.append(end)

def dijkstra():
    
    
def get_closest(source, matrix):
    closest = float('inf')
    i = None
    for cust in matrix[source]:
        if (Distances.get_distance(source, cust) < closest) and (Distances.get_distance(source, cust) > 0) and (cust not in path):
            closest = Distances.get_distance(source, cust)
            i = cust
    print i
    return i


def get_nearest_neighbors(customers, source):
    path = [source]
    l = len(customers)
    while len(path) < l:
        path.append(get_next(source, customers, path))
        source = get_next(source, customers, path)
    return path
    
def get_next(source, customers, path):
    min = float('inf')
    next = source
    for i in range(len(customers)):
        if Distances.get_distance(customers.index(source), i) < min and customers.index(source) != i and customers[i] not in path:
            next = customers[i]
            min = Distances.get_distance(customers.index(source), i)
    return next
    


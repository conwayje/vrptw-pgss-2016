from ImportCustomers import import_customers
from Distances import Distances
from Customer import Customer
from Depot import Depot
from copy import deepcopy
from Visual import Visual
#nearest neighbors works

#may use this
def create_graph(customers):
    g = {}
    for c in customers:
        print('graphing')
        g[c] = {}
        for d in customers:
            g[c][d] = d.distance_to_customer(c)
    return g


def dijkstra(customers, source):
    d={}
    unvisited = []
    for c in customers:
        d[c] = float('inf')
        unvisited.append(c)
    d[source] = 0
    for c in unvisited:
       d[c] = c.distance_to_customer(source)
       
    # @TODO -- what is the deal with this thing ((o_O))

def get_closest(source, matrix):
    closest = float('inf')
    i = None
    for cust in matrix[source]:
        if (Distances.get_distance(source, cust) < closest) and (Distances.get_distance(source, cust) > 0) and (cust not in path):
            closest = Distances.get_distance(source, cust)
            i = cust
    print i
    return i
    
def get_nearest_neighbors_all_trucks(customers, source, numtrucks):
    l = len(customers)
    print l
    plen = 1
    paths = [ [source] for t in range(numtrucks) ]
    
    while (plen < l):
        for path in paths:
            if plen < l:
                path.append(get_next(path[-1], customers, paths))
                plen += 1
            #print "path"
            #print path
            #unvisited.pop(source)
    for path in paths: print path 
    for path in paths: print len(path) 
    return paths
            

def get_nearest_neighbors(customers, source):
    path = [source]
    l = len(customers)
    while len(path) < l:
        path.append(get_next_one_path(source, customers, path))
        source = get_next_one_path(source, customers, path)
    return Path(path)

def get_next(source, customers, paths):

    min = float('inf')
    next = source
    for i in range(len(customers)):
        if Distances.get_distance(customers.index(source), i) < min and customers.index(source) != i and customers[i] not in paths[0] and customers[i] not in paths[1] and customers[i] not in paths[2]:
            next = customers[i]
            min = Distances.get_distance(customers.index(source), i)
    return next
    
def get_next_one_path(source, customers, paths):

    min = float('inf')
    next = source
    for i in range(len(customers)):
        if Distances.get_distance(customers.index(source), i) < min and customers.index(source) != i and customers[i] not in path:
            next = customers[i]
            min = Distances.get_distance(customers.index(source), i)
    return next


custs = import_customers("C201.txt")
depot = Customer(0, 0, 0, 0, 0, 0, 0) # @HACK
c = [depot]
for cust in custs:
    c.append(cust)
Distances.calculate_matrix(custs)
get_nearest_neighbors_all_trucks(c, depot, 3)
from ImportCustomers import import_customers
from Distances import Distances
<<<<<<< HEAD
from Customer import distance_to_customer
=======
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
    matrix = Distances.calculate_matrix(customers)
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
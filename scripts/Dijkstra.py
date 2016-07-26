from ImportCustomers import import_customers
from Distances import Distances
from Customer import Customer
from Depot import Depot
from copy import deepcopy
from Visual import Visual
#from State import State
from Truck import Truck
from Path import Path

#nearest neighbors works

class Dijsktra():

    @staticmethod
    def get_nearest_neighbors_all_trucks(customers, source, num_trucks):
        l = len(customers)
        plen = 1
        paths = [[source] for t in range(num_trucks)]

        # All trucks simultaneously
        while (plen < l):
            for path in paths:
                if plen < l:
                    path.append(Dijsktra.get_next(path[-1], customers, paths))
                    plen += 1

        return paths

    @staticmethod
    def get_nearest_neighbors(customers, source):
        path = [source]
        l = len(customers)
        while len(path) < l:
            path.append(Dijsktra.get_next_one_path(source, customers, path))
            source = Dijsktra.get_next_one_path(source, customers, path)
        return Path(path)

    @staticmethod
    def get_next(source, customers, paths):

        min = float('inf')
        next = source
        for i in range(len(customers)):
            if Distances.get_distance(customers.index(source), i) < min and customers.index(source) != i and customers[i] not in paths[0] and customers[i] not in paths[1] and customers[i] not in paths[2]:
                next = customers[i]
                min = Distances.get_distance(customers.index(source), i)
        return next
        
    @staticmethod
    def get_next_random(source, customers, path):
        closest = sorted(customers, key=lambda: Distances.get_distance(source.number, customer.number))
        closest_few = closest[:3]
        r = randint(0,len(closest_few))
        return closest_few[r]

    @staticmethod
    def get_next_one_path(source, customers, path):
        min = float('inf')
        next = source
        for i in range(len(customers)):
            if Distances.get_distance(customers.index(source), i) < min and customers.index(source) != i and ( customers[i] not in path):
                next = customers[i]
                min = Distances.get_distance(customers.index(source), i)
        return next
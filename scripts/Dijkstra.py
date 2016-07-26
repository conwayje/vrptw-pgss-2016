from ImportCustomers import import_customers
from Distances import Distances
from Customer import Customer
from Depot import Depot
from copy import deepcopy
from Visual import Visual
#from State import State
from Truck import Truck
from Path import Path
from random import randint

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
    def get_nearest_neighbors_random(customers, source, num_trucks, numrandom):
        l = len(customers)
        plen = 1
        paths = [[source] for t in range(num_trucks)]
        # All trucks simultaneously
        while (plen < l):
            for path in paths:
                if plen < l:
                    path.append(Dijsktra.get_next_random(path[-1], customers, paths, numrandom))
                    plen += 1
        return paths
        
    @staticmethod
    def get_next(source, customers, paths):

        min = float('inf')
        next = source
        all_paths = []
        for p in range(len(paths)):
            path = paths[p]
            for c in range(len(path)):
                all_paths.append(path[c])
                
        for i in range(len(customers)):
            if Distances.get_distance(customers.index(source), i) < min and customers.index(source) != i and customers[i] not in all_paths:
                next = customers[i]
                min = Distances.get_distance(customers.index(source), i)
        return next
        
    @staticmethod
    def get_next_random(source, customers, paths, numrandom):
        all_paths = []
        for p in range(len(paths)):
            path = paths[p]
            for c in range(len(path)):
                all_paths.append(path[c])
        
        closest = sorted(customers, key=lambda customer: Distances.get_distance(source.number, customer.number))
        closest_good = []

        for c in closest:
            if c in all_paths:
                pass
            else:
                closest_good.append(c)
        
        closest_few = closest_good[:numrandom]
        r = randint(0, len(closest_few)-1)
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
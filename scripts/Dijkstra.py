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
    # may use this
    def create_graph(customers):
        g = {}
        for c in customers:
            print('graphing')
            g[c] = {}
            for d in customers:
                g[c][d] = d.distance_to_customer(c)
        return g

    @staticmethod
    def dijkstra(customers, source):
        d = {}
        unvisited = []
        for c in customers:
            d[c] = float('inf')
            unvisited.append(c)
        d[source] = 0
        for c in unvisited:
            d[c] = c.distance_to_customer(source)
            # @TODO -- what is the deal with this thing ((o_O))

    @staticmethod
    def get_nearest_neighbors_all_trucks(customers, source, numtrucks):
        l = len(customers)
        print l
        plen = 1
        paths = [[source] for t in range(numtrucks)]

        # All trucks simultaneously
        while (plen < l):
            for path in paths:
                if plen < l:
                    path.append(Dijsktra.get_next(path[-1], customers, paths))
                    plen += 1
                print "path"
                print path
                # unvisited.pop(source)

        # One truck at a time
        # for path in paths:
        #     plen = 1
        #     while (plen < l / numtrucks):
        #         plen += 1
        #         path.append(get_next(path[-1], customers, paths))

        #for path in paths: print path
        #for path in paths: print len(path)

        # @TODO Fix trucks
        #state = State([Truck(1, 0, 0, 700, path=Path(paths[0][1:])),
        #              Truck(2, 0, 0, 700, path=Path(paths[1][1:])),
        #              Truck(3, 0, 0, 700, path=Path(paths[2][1:]))], parent=None)
        #state.plot()
        #return state
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
    def get_next_one_path(source, customers, path):

        min = float('inf')
        next = source
        for i in range(len(customers)):
            if Distances.get_distance(customers.index(source), i) < min and customers.index(source) != i and ( customers[i] not in path):
                next = customers[i]
                min = Distances.get_distance(customers.index(source), i)
        return next
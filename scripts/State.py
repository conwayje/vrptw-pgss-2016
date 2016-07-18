from Visual import Visual
from Truck import Truck
import copy
import math
from Path import Path
from Depot import Depot
from random import randint, randrange, choice
import random

class State():

    # @TODO -- truck number dependency
    def __init__(self, truck1, truck2, truck3, parent = None):

        # @TODO -- truck number dependency
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.paths = [truck1.path, truck2.path, truck3.path]
        self.distance = None
        self.parent = parent
        #  @TODO -- should we also maintain children...?

        #  @TODO -- similar to reason above:  maintain score(?)

    def calculate_distance(self):
        self.distance = self.truck1.path.distance + self.truck2.path.distance + self.truck3.path.distance
        return self.distance

    def plot(self):
        # @TODO -- truck number dependency
        Visual.plot_path(self.truck1.path, color='g')
        Visual.plot_path(self.truck2.path, color='c')
        Visual.plot_path(self.truck3.path, color='m')
        Visual.show()

    def plot_missed(self):
        # @TODO -- truck number dependency
        Visual.plot_customers(Depot(0,0), self.truck1.path.is_valid())
        Visual.plot_customers(Depot(0,0), self.truck2.path.is_valid())
        Visual.plot_customers(Depot(0,0), self.truck3.path.is_valid())
        Visual.show()

    # @TODO -- point to heuristic score
    def get_score(self):
        missed_customer_penalty = 10**6

        # @TODO -- truck number dependency
        paths = [self.truck1.path, self.truck2.path, self.truck3.path]

        score = sum( [path.distance for path in paths] )

        for path in paths:
            score += len( path.is_valid() ) * missed_customer_penalty

        return score

    # @TODO -- still lots to do here, of course ;)
    def get_children(self):
        children = [] # list of states
        children_paths = []
        paths = self.paths

        # these ones probably aren't good
        # children_paths += State.cycle_three_four_times(paths)
        # children_paths += State.redistribute_more_evenly( paths )

        # these ones are probably good
        children_paths += State.shuffle( paths, 5 )
        children_paths += State.sort_paths( paths )
        children_paths += State.path_swap( paths )
        children_paths += State.distance_swap( paths )
        children_paths += State.switch_between_paths( paths, 15 )

        # child_paths should be a list containing three paths per entry (as a list)
        for child_paths in children_paths:
            # @TODO -- truck number dependency
            children.append(
            State(Truck(1, 0, 0, 700, child_paths[0]), Truck(2, 0, 0, 700, child_paths[1]) ,Truck(3, 0, 0, 700, child_paths[2])))

        return children

    @staticmethod #medium move
    # @TODO -- truck number dependency (entire function)
    def cycle_three_four_times(paths):
        children = []

        for i in range(15):
            route1 = paths[0].route
            route2 = paths[1].route
            route3 = paths[2].route
            length1 = len(route1)
            length2 = len(route2)
            length3 = len(route3)
            for i in range(0,4):
                rand1 = randint(0,length1-1)
                rand2 = randint(0,length2-1)
                rand3 = randint(0,length3-1)
                temp = route1[rand1]
                route1[rand1] = route2[rand2]
                route2[rand2] = route3[rand3]
                route3[rand3] = temp
            new_paths = [Path(route1), Path(route2), Path(route3)]
            children.append(new_paths)
            return children

    @staticmethod #small move
    def redistribute_more_evenly(paths):
        """ For ex, with 100 customers and 3 trucks, we expect 33 per truck.  Siphon off the
            surplus for any 'overloaded' paths and then add some surplus randomly into 'underloaded'
            paths """
        children = []

        expected = sum( [ len(element.route) for element in paths] ) / len(paths)
        overserved_paths = []
        underserved_paths = []
        surplus = 0

        for path in paths:
            if len( path.route ) > expected:
                overserved_paths.append( path )
                surplus += len( path.route ) - expected
            else:
                underserved_paths.append( path )

        # create 5 different moves
        for k in range(5):
            # create copies of the routes
            copy_overserved = [ copy.deepcopy(path.route) for path in overserved_paths ]
            copy_underserved = [ copy.deepcopy(path.route) for path in underserved_paths ]
            # move a total of [surplus] things from overserved routes to underserved routes
            for i in range(surplus):
                overserved_path = choice( copy_overserved )
                underserved_path = choice( copy_underserved )
                customer_to_move = overserved_path.pop( randrange( len ( overserved_path ) ) )
                underserved_path.insert( randrange( len( underserved_path ) ), customer_to_move )

            children.append([ Path( element ) for element in copy_underserved ] + [ Path( element ) for element in copy_overserved ])

        # a list containing lists-of-paths
        return children

    @staticmethod #big move
    def shuffle(paths, by_num):
        children = []

        for i in range(7):
            new_paths = []
            for path in paths:
                route = []
                for i in range(0, len(path.route), by_num - 1):
                    custs = path.route[i:i+by_num-1]
                    random.shuffle(custs, random.random)
                    for cust in custs:
                        route.append(cust)
                new_path = Path(route)

                new_paths.append(new_path)

            children.append(new_paths)

        return children

    @staticmethod #small move
    # check if swaps can make the paths valid if they weren't, tolerance controls added distance
    #this used to be get_fixed_children
    def sort_paths(paths):
        children = []

        pathnum = 0

        for path in paths:
            i = 0
            p = copy.deepcopy(path)
            prevtime = 0

            new_paths =  copy.deepcopy(paths)


            new_paths[pathnum] = Path(sorted(p.route, key = lambda customer: customer.close_time))

            is_sorted = True
            for i in range(min(len(new_paths[pathnum].route), len(p.route))):
                if not (new_paths[pathnum].route[i].x == p.route[i].x and new_paths[pathnum].route[i].y ==   p.route[i].y):
                    is_sorted = False

            if not is_sorted:
                children.append(new_paths)

            pathnum += 1

        return children

    @staticmethod #small move
    def path_swap(paths):
        new_path_sets = []

        for i in range( 15 ):
            new_paths = copy.deepcopy( paths )
            # get two unique random paths
            path_a_index = randint(0, 2)
            # @TODO -- truck number dependency
            path_b_index = (path_a_index + randint(1, 2)) % 3
            path_a = new_paths[path_a_index]
            path_b = new_paths[path_b_index]
            # select two customers
            customer_a = randint(0, len(path_a.route) - 1)
            customer_b = randint(0, len(path_b.route) - 1)
            path_a.route[customer_a], path_b.route[customer_b] = path_b.route[customer_b], path_a.route[customer_a]
            new_path_sets.append(new_paths)

        return new_path_sets

    @staticmethod #small move
    def distance_swap(paths):
        children = []
        for i in range( 15 ):
            new_paths = [copy.deepcopy(element) for element in paths]
            # @TODO -- truck number dependency
            path_index = randint(0, 2)
            path = new_paths[path_index]
            # gets two random customers, if the first is farther then the secondthen swap
            customer_a = randint(0, len(path.route) - 1)
            customer_b = randint(customer_a, len(path.route) - 1)
            if path.route[customer_a].distance() > path.route[customer_b].distance():
                path.route[customer_a], path.route[customer_b] = path.route[customer_b], path.route[customer_a]
            children.append(new_paths)
        return children

    @staticmethod #medium move, 3 children
    def five_section_swap(paths):
        children = []
        for j in range(len(paths)):
            path = paths[j]
            new_route = copy.deepcopy(path.route)
            section_to_swap = []
            index = randint(0, len(path)-6)
            for i in range(index, index+5):
                section_to_swap.append(path.route[i])
                new_route.remove(i)

            to_insert = randint(0, len(new_route) - 1)
            for k in range(to_insert, to_insert+5):
                new_route.insert(k)

            new_paths = copy.deepcopy(paths)
            new_paths[j] = Path(new_route)
            children.append(new_paths)


    @staticmethod #large move
    def alternating_shuffle_within_path(paths):
        children = []

        for j in range(len(paths)):
            path = paths[j]
            temp_route = copy.deepcopy(path.route)
            new_route = []
            while(len(temp_route) > 0):
                cust = temp_route.pop(0)
                new_route.append(cust)
                temp_route = sorted(temp_route, key = lambda customer: customer.distance_to_customer(cust))

            new_paths = copy.deepcopy(paths)
            new_paths[j] = Path(new_route)
            children.append(new_paths)

        return children

    @staticmethod
    def switch_between_paths(paths, numtoswap):
        new_path_lists = []

        for k in range(10):
            p = copy.deepcopy(paths)

            for i in range(numtoswap):
                # @TODO -- truck number dependency
                path_a = randint(0, 2)
                path_b = randint(0, 2)

                cust_a = randint(0, len(p[path_a].route) - 1)
                cust_b = randint(0, len(p[path_b].route) - 1)

                temp = p[path_a].route[cust_a]
                p[path_a].route[cust_a] = p[path_b].route[cust_b]
                p[path_b].route[cust_b] = temp

            new_path_lists.append( p )

        return new_path_lists

    def __repr__(self):
        return "\n<State: Truck 1: {0}\nTruck2: {1}\nTruck3:{2}>".format(self.truck1.path.route, self.truck2.path.route, self.truck3.path.route)


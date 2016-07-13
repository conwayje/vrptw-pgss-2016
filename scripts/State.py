from Visual import Visual
from Truck import Truck
import copy
import math
from Path import Path
from Depot import Depot
from random import randint, randrange, choice
import ipdb
import random

class State():

    def __init__(self, truck1, truck2, truck3, parent = None):
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.paths = [truck1.path, truck2.path, truck3.path]
        self.distance = None
        self.parent = parent
        #  @TODO -- should we also maintain children...?

        #  @TODO -- similar to reason above:  maintain score(?)

    def calculate_distance(self):
        self.distance = self.truck1.path.calculate_distance() + self.truck2.path.calculate_distance() + self.truck3.path.calculate_distance()
        return self.distance

    def plot(self):
        Visual.plot_path(self.truck1.path, color='g')
        Visual.plot_path(self.truck2.path, color='c')
        Visual.plot_path(self.truck3.path, color='m')
        Visual.show()

    def plot_missed(self):
        Visual.plot_customers(Depot(0,0), self.truck1.path.is_valid())
        Visual.plot_customers(Depot(0,0), self.truck2.path.is_valid())
        Visual.plot_customers(Depot(0,0), self.truck3.path.is_valid())
        Visual.show()

    # @TODO -- point to heuristic score
    def get_score(self):
        missed_customer_penalty = 10**6

        paths = [self.truck1.path, self.truck2.path, self.truck3.path]

        score = sum( [path.calculate_distance() for path in paths] )

        for path in paths:
            score += len( path.is_valid() ) * missed_customer_penalty

        return score

    # @TODO -- still lots to do here, of course ;)
    def get_children(self):
        children = [] # list of states
        children_paths = []
        paths = [self.truck1.path, self.truck2.path, self.truck3.path]

        #children_paths = State.cycle_three_four_times(paths, children_paths)
        children_paths = State.shuffle_in_fives( paths, children_paths )
        children_paths = State.get_fixed_children( paths, children_paths, 100 )
        # child_paths should be a list containing three paths per entry (as a list)
        for child_paths in children_paths:
            children.append(
            State(Truck(1, 0, 0, 700, child_paths[0]), Truck(2, 0, 0, 700, child_paths[1]) ,Truck(3, 0, 0, 700, child_paths[2])))

    @staticmethod
    def cycle_three(paths):
        route1 = paths[0].route
        route2 = paths[1].route
        route3 = paths[2].route
        length1 = len(route1)
        length2 = len(route2)
        length3 = len(route3)
        rand1 = randint(0,length1-1)
        rand2 = randint(0,length2-1)
        rand3 = randint(0,length3-1)
        temp = route1[rand1]
        route1[rand1] = route2[rand2]
        route2[rand2] = route3[rand3]
        route3[rand3] = temp
        return [Path(route1), Path(route2), Path(route3)]

        return children

    @staticmethod

    def cycle_three_four_times(paths, children):
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


    def redistribute_more_evenly(self, children, paths):
        """ For ex, with 100 customers and 3 trucks, we expect 33 per truck.  Siphon off the
            surplus for any 'overloaded' paths and then add some surplus randomly into 'underloaded'
            paths """
        expected = sum( [ len(element.route) for element in self.paths] ) / len( self.paths )
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
            # create copies of the paths
            copy_overserved = [ copy.deepcopy(path.route) for path in overserved_paths ]
            copy_underserved = [ copy.deepcopy(path.route) for path in underserved_paths ]
            # move a total of [surplus] things from overserved routes to underserved routes
            for i in range(surplus):
                overserved_path = choice( copy_overserved )
                underserved_path = choice( copy_underserved )
                customer_to_move = overserved_path.pop( randrange( len ( overserved_path ) ) )
                underserved_path.insert( randrange( len( underserved_path ) ), customer_to_move )

            children += [ [ Path( element ) for element in copy_underserved ] + [ Path( element ) for element in copy_overserved ] ]

        return children

    @staticmethod
    def shuffle_in_fives(paths, children):
        for i in range(7):
            new_paths = []
            for path in paths:
                route = []
                for i in range(0, len(path.route), 4):
                    custs = path.route[i:i+4]
                    random.shuffle(custs, random.random)
                    for cust in custs:
                        route.append(cust)
                new_path = Path(route)

                new_paths.append(new_path)

            children.append(new_paths)

        #ipdb.set_trace()

        return children


    # check if swaps can make the paths valid if they weren't, tolerance controls added distance
    def sort_paths(paths):
        children = [] #list of states

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

            # for cust in p.route:
            #     time = p.get_arrival_time_of_customer(cust)
            #     diff = time - prevtime
            #     if diff > 120 and i != len(p.route):
            #         temp = sorted(p.route[i:], key = lambda customer: customer.close_time)[0]
            #         p.route[p.route.index(temp)] = p.route[i]
            #         p.route[i] = temp
            #         new_paths =  copy.deepcopy(paths)
            #         new_paths[pathnum] = p
            #         children.append(new_paths)
            #
            #     prevtime = time
            #     i += 1
            pathnum += 1

        return children

    @staticmethod
    def switch_between_paths(paths, numtoswap):


        p = copy.deepcopy(paths)

        for i in range(numtoswap):
            path_a = randint(0,2)
            path_b = randint(0,2)

            cust_a = randint(0, len(p[path_a].route) -1)
            cust_b = randint(0, len(p[path_b].route) - 1)

            temp = p[path_a].route[cust_a]
            p[path_a].route[cust_a] = p[path_b].route[cust_b]
            p[path_b].route[cust_b] = temp


        return p

    def path_swap(paths, children):
        for i in range( 15 ):
            new_paths = [copy.deepcopy(element) for element in paths]
            # get two unique random paths
            path_a_index = randint(0, 2)
            path_b_index = (path_a_index + randint(1, 2)) % 3
            path_a = new_paths[path_a_index]
            path_b = new_paths[path_b_index]
            # select two customers
            customer_a = randint(0, len(path_a.route) - 1)
            customer_b = randint(0, len(path_b.route) - 1)
            path_a.route[customer_a], path_b.route[customer_b] = path_b.route[customer_b], path_a.route[customer_a]
            children.append(new_paths)
        return children

    @staticmethod
    def distance_swap(paths, children):
        for i in range( 15 ):
            new_paths = [copy.deepcopy(element) for element in paths]
            path_index = randint(0, 2)
            path = new_paths[path_index]
            # gets two random customers, if the first is farther then the secondthen swap
            customer_a = randint(0, len(path.route) - 1)
            customer_b = randint(customer_a, len(path.route) - 1)
            if path.route[customer_a].distance() > path.route[customer_b].distance():
                path.route[customer_a], path.route[customer_b] = path.route[customer_b], path.route[customer_a]
            children.append(new_paths)
        return children

    def is_world_record(self):
        # for c in self.truck1.path.route:
        #     print c.number,
        #
        # print "\n"
        # for c in self.truck2.path.route:
        #     print c.number,
        #
        # print "\n"
        # for c in self.truck3.path.route:
        #     print c.number,


        return (self.calculate_distance() < 591.55)

        # return self.get_score() <= 0


    def __repr__(self):
        return "\n<State: Truck 1: {0}\nTruck2: {1}\nTruck3:{2}>".format(self.truck1.path.route, self.truck2.path.route, self.truck3.path.route)


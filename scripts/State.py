from Visual import Visual
from Truck import Truck
import copy
import math
from Path import Path
from random import randint
import ipdb
import random

class State():

    def __init__(self, truck1, truck2, truck3, parent = None):
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.distance = None
        self.parent = parent
        #  @TODO -- should we also maintain children...?
        #  @TODO -- similar to Path, might want to store distance so that we don't have to
        #  do repetitive/useless/wasted calculations several times.  just access a value instead -- DONE

        #  @TODO -- similar to reason above:  maintain score(?)

    def calculate_distance(self):
        # @TODO -- if we do store distance, might want to set it here? -- DONE
        self.distance = self.truck1.path.calculate_distance() + self.truck2.path.calculate_distance() + self.truck3.path.calculate_distance()
        return self.distance

    def plot(self):
        Visual.plot_path(self.truck1.path, color='g')
        Visual.plot_path(self.truck2.path, color='c')
        Visual.plot_path(self.truck3.path, color='m')
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

        #ipdb.set_trace()

        for child_paths in children_paths:
            # ipdb.set_trace()
            children.append(
            State(Truck(1, 0, 0, 700, child_paths[0]), Truck(2, 0, 0, 700, child_paths[1]) ,Truck(3, 0, 0, 700, child_paths[2])))


        return children

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
    @staticmethod
    def get_fixed_children(paths, children, tolerance):

        # @TODO -- this is clever, but it takes
        # waaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaay too long.
        # try to find a logical shortcut, but keep in mind
        # that even if you have to execute the shortcut 15x
        # before you get it right once, that's still fine if it
        # only takes 2ms per execution.
        # for i in range(len(paths)):
        #     path = copy.deepcopy(paths[i])
        #     missed = path.is_valid()
        #     # print i, tempPath

        #     for m in missed:
        #         x = m.x
        #         y = m.y

        #         for cust in path.route:
        #             if(cust != m):

        #                 addedDistance = 0
        #                 custi = path.route.index(cust)
        #                 mi = path.route.index(m)

        #                 # new distances of liens that are affected swap
        #                 addedDistance += cust.distance_to_customer(path.route[mi-1]) if mi != 0 else math.hypot(cust.x, cust.y)
        #                 addedDistance += cust.distance_to_customer(path.route[mi+1]) if mi != len(path.route)-1 else math.hypot(cust.x, cust.y)
        #                 addedDistance += path.route[mi].distance_to_customer(path.route[custi+1]) if custi != len(path.route)-1 else math.hypot(m.x, m.y)
        #                 addedDistance += path.route[mi].distance_to_customer(path.route[custi+1]) if custi != len(path.route)-1 else math.hypot(m.x, m.y)

        #                 # old distances,
        #                 addedDistance -= path.distance_to_previous(cust)
        #                 addedDistance -= path.distance_to_next(cust)
        #                 addedDistance -= path.distance_to_previous(m)
        #                 addedDistance -= path.distance_to_next(m)

        #                 # print i, mi, m.number, path.get_arrival_time_of_customer(m),  cust.close_time, "\t"
        #                 if path.get_arrival_time_of_customer(m) < cust.close_time or True:
        #                     if(addedDistance < tolerance or True):
        #                         tempPath = Path(copy.deepcopy(path.route))
        #                         temp = tempPath.route[mi]
        #                         tempPath.route[mi] = tempPath.route[custi]
        #                         tempPath.route[custi] = temp
        #                         new_paths = copy.deepcopy(paths)
        #                         new_paths[i] = tempPath
        #                         if(len(new_paths[i].is_valid()) < len(path.is_valid())):
        #                             children.append(new_paths)


        ############################
        ######## NOTE ##############
        ############################
        #
        #
        #
        # this is EXTREMELY naive.
        # y'all should be more clever ;)
        # i don't mind if you delete this
        # as long as it's replaced w/
        # something more clever,
        # where clever = working + fast
        #
        #
        #
        # create somewhere between 20 and 50 children
        for i in range( 15 ):
            new_paths = [ copy.deepcopy( element ) for element in paths ]
            path_a = new_paths[ randint(0, 2) ]
            path_b = new_paths[ randint(0, 2) ]
            customer_a = randint( 0, len( path_a.route ) - 1 )
            customer_b = randint( 0, len( path_b.route ) - 1 )
            # switch them

            path_a.route[ customer_a ], path_b.route[ customer_b ] = path_b.route[ customer_b ], path_a.route[ customer_a ]

            children.append( new_paths )

        return children

    def is_world_record(self):
        # return (self.calculate_distance() < 591)
        return self.get_score() <= 0


    def __repr__(self):
        return "<State: Truck 1: {0}\nTruck2: {1}\nTruck3:{2}>".format(self.truck1.path.route, self.truck2.path.route, self.truck3.path.route)

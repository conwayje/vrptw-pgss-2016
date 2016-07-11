from Visual import Visual
from Truck import Truck
import copy
import math
from Path import Path
from random import randint
# import ipdb

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
        paths = [self.truck1.path, self.truck2.path, self.truck3.path]

        child_paths = State.sort_paths(paths)

        for i in range(20):
            child_paths.append(State.switch_between_paths(paths,1))


        for child_path in child_paths:
            children.append(
            State(Truck(1, 0, 0, 700, child_path[0]), Truck(2, 0, 0, 700, child_path[1]) ,Truck(3, 0, 0, 700, child_path[2])))

        return children

    @staticmethod
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


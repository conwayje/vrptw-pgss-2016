from Visual import Visual
from Truck import Truck
import copy
import math
from Path import Path

class State():

    def __init__(self, truck1, truck2, truck3, parent = None):
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.distance = None
        self.parent = parent
        # @TODO -- should we also maintain children...?
        #  @TODO -- similar to Path, might want to store distance so that we don't have to
        #  do repetitive/useless/wasted calculations several times.  just access a value instead -- DONE

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
        # return self.calculate_distance()
        paths = [self.truck1.path, self.truck2.path, self.truck3.path]
        missed = 100
        for path in paths:
            missed -= len(path.route) - len(path.is_valid())
        return missed

    # @TODO -- still lots to do here, of course ;)
    def get_children(self):
        children = [] # list of states
        paths = [self.truck1.path, self.truck2.path, self.truck3.path]


        for child_paths in State.get_fixed_children(paths, 100):
            children.append(
            State(Truck(1, 0, 0, 700, child_paths[0]), Truck(2, 0, 0, 700, child_paths[1]) ,Truck(3, 0, 0, 700, child_paths[2])))

        return children



    @staticmethod
    # check if swaps can make the paths valid if they weren't, tolerance controls added distance
    def get_fixed_children(paths, tolerance):
        children = [] #list of states
        for i in range(len(paths)):
            path = copy.deepcopy(paths[i])
            missed = path.is_valid()
            # print i, tempPath

            for m in missed:
                x = m.x
                y = m.y

                for cust in path.route:
                    if(cust != m):

                        addedDistance = 0
                        custi = path.route.index(cust)
                        mi = path.route.index(m)

                        # new distances of liens that are affected swap
                        addedDistance += cust.distance_to_customer(path.route[mi-1]) if mi != 0 else math.hypot(cust.x, cust.y)
                        addedDistance += cust.distance_to_customer(path.route[mi+1]) if mi != len(path.route)-1 else math.hypot(cust.x, cust.y)
                        addedDistance += path.route[mi].distance_to_customer(path.route[custi+1]) if custi != len(path.route)-1 else math.hypot(m.x, m.y)
                        addedDistance += path.route[mi].distance_to_customer(path.route[custi+1]) if custi != len(path.route)-1 else math.hypot(m.x, m.y)

                        # old distances,
                        addedDistance -= path.distance_to_previous(cust)
                        addedDistance -= path.distance_to_next(cust)
                        addedDistance -= path.distance_to_previous(m)
                        addedDistance -= path.distance_to_next(m)

                        # print i, mi, m.number, path.get_arrival_time_of_customer(m),  cust.close_time, "\t"
                        if path.get_arrival_time_of_customer(m) < cust.close_time or True:
                            if(addedDistance < tolerance or True):
                                tempPath = Path(copy.deepcopy(path.route))
                                temp = tempPath.route[mi]
                                tempPath.route[mi] = tempPath.route[custi]
                                tempPath.route[custi] = temp
                                new_paths = copy.deepcopy(paths)
                                new_paths[i] = tempPath
                                if(len(new_paths[i].is_valid()) < len(path.is_valid())):
                                    children.append(new_paths)

        return children

    def is_world_record(self):
        # return (self.calculate_distance() < 591)
        return self.get_score() <= 0


    def __repr__(self):
        return "<State: Truck 1: {0}\nTruck2: {1}\nTruck3:{2}>".format(self.truck1.path.route, self.truck2.path.route, self.truck3.path.route)

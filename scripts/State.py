from Visual import Visual
from Truck import Truck
import copy
import math

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
        self.distance = self.truck1.path.get_distance() + self.truck2.path.get_distance() + self.truck3.path.get_distance()
        return self.distance

    def plot(self):
        Visual.plot_path(self.truck1.path, color='g')
        Visual.plot_path(self.truck2.path, color='c')
        Visual.plot_path(self.truck3.path, color='m')
        Visual.show()

    # @TODO -- point to heuristic score
    def get_score(self):
        return self.calculate_distance()

    # @TODO -- still lots to do here, of course ;)
    def get_children(self):
        children = [] # list of states
        paths = [self.truck1.path, self.truck2.path, self.truck2.path]
        State.get_fixed_children(paths, 50)


    @staticmethod
    # check if swaps can make the paths valid if they weren't, tolerance controls added distance
    def get_fixed_children(paths, tolerance):
        children = [] #list of states

        for i in len(paths):
            tempPath = copy.deepcopy(paths[i])
            missed = tempPath.is_valid()
            for m in missed:
                x = m.x
                y = m.y
                for cust in tempPath:
                    if(cust != m):
                        addedDistance = 0
                        custi = tempPath.index(cust)
                        mi = tempPath.index(m)


                        # new distances of liens that are affected swap
                        addedDistance += cust.distance_to_customer(tempPath[mi-1 if mi != 0 else math.hypot(cust.x, cust.y) ])
                        addedDistance += cust.distance_to_customer(tempPath[mi+1 if mi != len(tempPath)-1 else math.hypot(cust.x, cust.y) ])
                        addedDistance += mi.distance_to_customer(tempPath[custi+1 if custi != len(tempPath)-1 else math.hypot(m.x, m.y) ])
                        addedDistance += mi.distance_to_customer(tempPath[custi+1 if custi != len(tempPath)-1 else math.hypot(m.x, m.y) ])

                        # old distances,
                        addedDistance -= tempPath.distance_to_prev(cust)
                        addedDistance -= tempPath.distance_to_next(cust)
                        addedDistance -= tempPath.distance_to_prev(m)
                        addedDistance -= tempPath.distance_to_next(m)

                        if tempPath.get__arrival_time_of_customer(m) < cust.close_time:
                            if(addedDistance < tolerance):
                                pass #make new states




    def __repr__(self):
        return "<State: Truck 1: {0}\nTruck2: {1}\nTruck3:{2}>".format(self.truck1.route, self.truck2.route, self.truck3.route)


from Visual import Visual
from Truck import Truck
import copy

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

        i = 0
        # first check if swaps can make the paths valid if they weren't
        for path in paths:
            tempPath = copy.deepcopy(path)
            missed = tempPath.is_valid()

            for m in missed:
                x = m.x
                y = m.y

                for cust in path.route:
                    if cust != m:
                       tempPath.route[tempPath.index(m)]




    def __repr__(self):
        return "<State: Truck 1: {0}\nTruck2: {1}\nTruck3:{2}>".format(self.truck1.route, self.truck2.route, self.truck3.route)


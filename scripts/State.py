from Visual import Visual
from Truck import Truck
import copy

class State():

    def __init__(self, truck1, truck2, truck3, parent = None):
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.parent = parent

    def get_distance(self):
        return self.truck1.path.get_distance() + self.truck2.path.get_distance() + self.truck3.path.get_distance()

    def plot(self):
        Visual.plot_path(self.truck1.path, color='g')
        Visual.plot_path(self.truck2.path, color='c')
        Visual.plot_path(self.truck3.path, color='m')
        Visual.show()

    #TODO
    def get_score(self):
        return self.get_distance()

    #TODO
    def get_children(self):
        children = []
        paths = [self.truck1.path, self.truck2.path, self.truck2.path]

        for path in paths:
            tempPath = copy.deepcopy(path)
            missed = tempPath.is_valid()
            for m in missed:
                x = m.x
                y = m.y
                 


    def __str__(self):
        return "<State: Truck 1: {0}\nTruck2: {1}\nTruck3:{2}>".format(self.truck1.route, self.truck2.route, self.truck3.route)
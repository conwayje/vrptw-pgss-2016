class State():

    def __init__(self, truck1, truck2, truck3, parent = None):
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.parent = parent

    def get_distance(self):
        return self.truck1.path.get_distance() + self.truck2.path.get_distance() + self.truck3.path.get_distance()

    def get_children(self):
        pass
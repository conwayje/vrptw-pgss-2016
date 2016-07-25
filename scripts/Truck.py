from Path import Path

class Truck():

    def __init__(self, number, x, y, cargo, path = None, distance = None):
        self.number = number #truck id/number
        self.x = x #x location
        self.y = y #y location
        self.cargo = cargo #amount of cargo currently in truck
        self.path = path #path object
        self.distance = distance #total distance traveled

    def __repr__(self):
        return "<Truck {0}: ({1}, {2}), cargo = {3}, path = {4}, distance = {5}>".format(self.number, self.x, self.y, self.cargo, self.path, self.distance)

    # @TODO -- refer to distance matrix instead
    @staticmethod
    def distance_from_depot(truck): #distance from depot
        return (truck.y**2 + truck.x**2)**0.5

    @staticmethod
    def get_index_customer_missed(truck, cargo):
        return truck.path.get_index_customer_missed(truck.cargo)
        
    def cargo_left(self):
        if(self.cargo - self.path.cargo_used() < 0):
            return self.cargo - self.path.cargo_used()
        return 0

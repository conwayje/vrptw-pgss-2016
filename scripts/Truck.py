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

    def distance_to_customer(self, cust): #distance to a given customer
        return ((cust.y - self.y)**2 + (cust.x - self.x)**2)**0.5

    def distance_from_depot(self): #distance from depot
        return (self.y**2 + self.x**2)**0.5

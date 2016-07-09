from Path import Path

class Truck():
    #class for Truck
    # @TODO -- note that cargo amount is 700 for one instance and 1000 for the other.
    # is this taken into account wherever Truck() objects are created?
    #
    # actually, it feels a little suspect to have a default on that either way.  i think that should
    # probably be a required argument to protect our future selves from our current selves
    def __init__(self, number, x, y, cargo = 700, path = None, distance = None):
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

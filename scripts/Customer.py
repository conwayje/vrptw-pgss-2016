""" Represents a customer and its location (x,y), its time window (open, close), service time, and demand.
"""

class Customer():

    def __init__(self, number, x, y, open_time, close_time, service_time, demand, cluster = None):
        self.number = number
        self.x = x
        self.y = y
        self.open_time = open_time
        self.close_time = close_time
        self.service_time = service_time
        self.demand = demand
        self.cluster = cluster

    def __repr__(self):
        #return "<Customer {0}: ({1}, {2}), open_time = {3}, close_time = {4}, service_time = {5}, demand = {6}>".format(self.number, self.x, self.y, self.open_time, self.close_time, self.service_time, self.demand)
        return "<Customer {0}: ({1}, {2}), [{3}, {4}]>".format(self.number, self.x, self.y, self.open_time, self.close_time)

    # @TODO -- this is fine because we need an initial way to get the distance from c1 to c2,
    # but otherwise we need either...
    # a) to never use this and refer only to the distance matrix, or
    # b) to have a method on Customer that refers directly to the distance matrix
    # My personal preference is to aim for (a) but to also have (b)
    def distance_to_customer(self, customer): #gets distance from one customer to another
        return ((customer.y - self.y)**2 + (customer.x - self.x)**2)**0.5

    def timewindow(self):
        return self.open_time
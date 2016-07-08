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

    def __str__(self):
        #return "<Customer {0}: x = {1}, y = {2}, open_time = {3}, close_time = {4}, service_time = {5}, demand = {6}>".format(self.number, self.x, self.y, self.open_time, self.close_time, self.service_time, self.demand)
        return "<Customer {0}: x = {1}, y = {2}>".format(self.number, self.x, self.y)

    def distance_to_customer(self, customer): #gets distance from one customer to another
        return ((customer.y - self.y)**2 + (customer.x - self.x)**2)**0.5
        
    def distance(self): #gets the customer's distance from depot
        return (self.y**2 + self.x**2)**0.5
        
    def closest_customers(self, cust):
        self = sorted(self, key = lambda customer: customer.distance_to_customer(cust))
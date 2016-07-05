# Jahnik and Dan
# Simple class to interact with a route/path of a truck
# Can return the total distance, customer at a certain time ..
#
class Path():
    def __init__(self, route):
        self.route = route

    def getDistance(self):
        distance = 0
        prevCustomer = None
        isFirstTime = True
        for customer in self.route:
            if isFirstTime:
                prevCustomer = customer
                isFirstTime = False
            else:
                distance += ((customer.x-prevCustomer.x)**2 + (customer.y-prevCustomer.y)**2)**.5
                prevCustomer = customer

    def g



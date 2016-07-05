# Jahnik and Dan
# Simple class to interact with a route/path of a truck
# Can return the total distance, customer at a certain time ..
# c was used as customer in order to avoid conflict with old code

import math

class Path():

    def __init__(self, route):
        self.route = route

    # returns the total distance
    def get_distance(self):
        distance = 0
        prevCustomer = None
        isFirstTime = True
        for c in self.route:
            if isFirstTime:
                prevCustomer = c
                isFirstTime = False
            else:
                distance += ((c.x-prevCustomer.x)**2 + (c.y-prevCustomer.y)**2)**.5
                prevCustomer = c

    # returns whether the truck makes it on time to every customer by returning
    # an array of the customers missed. If the path is valid, an empty array will be returned
    def is_valid(self):
        prevCustomer = None
        time = 0
        isFirstTime = True
        missedCustomers = []

        for c in self.route:
            if isFirstTime:
                # truck leaves from (0, 0)
                time = math.hypot(c.x, c.y)

                # if truck arrives before customer is open, assume truck waits
                if time < c.open_time:
                    time = c.open_time

                # if truck arrives late, return false
                if time > c.close_time:
                    missedCustomers.append(c)

                time += c.service_time
                isFirstTime = False
            else:
                time += ((c.x-prevCustomer.x)**2 + (c.y-prevCustomer.y)**2)**.5

                # if truck arrives before customer is open, assume truck waitds
                if time < c.open_time:
                    time = c.open_time

                # if truck arrives late, return false
                if time > c.close_time:
                    missedCustomers.append(c)

                time += c.service_time
                prevCustomer = c

        return missedCustomers

    # gets the customer the truck was last at
    def get_last_customer_visited(self, current_time):
        prevCustomer = None
        isFirstTime = True
        time = 0

        for c in self.route:
            if isFirstTime:

                # truck leaves from (0, 0)
                time = math.hypot(c.x, c.y)
                if(time > current_time):
                    return None

                # if truck arrives before customer is open, assume truck waits
                if time < c.open_time:
                    time = c.open_time
                time += c.service_time

                if(time > current_time):
                    return c

                isFirstTime = False
            else:
                time += ((c.x - prevCustomer.x) ** 2 + (c.y - prevCustomer.y) ** 2) ** .5

                if(time > current_time):
                    return prevCustomer

                # if truck arrives before customer is open, assume truck waitds
                if time < c.open_time:
                    time = c.open_time
                time += c.service_time

                if(time > current_time):
                    return c

                prevCustomer = c

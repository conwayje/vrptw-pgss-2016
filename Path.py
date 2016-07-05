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
        prev_customer = None
        is_first_time = True
        for c in self.route:
            if is_first_time:
                prev_customer = c
                is_first_time = False
            else:
                distance += ((c.x-prev_customer.x)**2 + (c.y-prev_customer.y)**2)**.5
                prev_customer = c

    # returns whether the truck makes it on time to every customer by returning
    # an array of the customers missed. If the path is valid, an empty array will be returned
    def is_valid(self):
        prev_customer = None
        time = 0
        is_first_time = True
        missedCustomers = []

        for c in self.route:
            if is_first_time:
                # truck leaves from (0, 0)
                time = math.hypot(c.x, c.y)

                # if truck arrives before customer is open, assume truck waits
                if time < c.open_time:
                    time = c.open_time

                # if truck arrives late, return false
                if time > c.close_time:
                    missedCustomers.append(c)

                time += c.service_time
                is_first_time = False
            else:
                time += ((c.x-prev_customer.x)**2 + (c.y-prev_customer.y)**2)**.5

                # if truck arrives before customer is open, assume truck waitds
                if time < c.open_time:
                    time = c.open_time

                # if truck arrives late, return false
                if time > c.close_time:
                    missedCustomers.append(c)

                time += c.service_time
                prev_customer = c

        return missedCustomers

    # gets the customer the truck was last at
    def get_last_customer_visited(self, current_time):
        prev_customer = None
        is_first_time = True
        time = 0

        for c in self.route:
            if is_first_time:

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

                is_first_time = False
            else:
                time += ((c.x - prev_customer.x) ** 2 + (c.y - prev_customer.y) ** 2) ** .5

                if(time > current_time):
                    return prev_customer

                # if truck arrives before customer is open, assume truck waitds
                if time < c.open_time:
                    time = c.open_time
                time += c.service_time

                if(time > current_time):
                    return c

                prev_customer = c

    # returns whether the path intersects itself
    def intersects_self(self):
        intersects = False
        points = [(0, 0)]
        for c in self.route:
            points.append((c.x, c.y))

        for i in range(1, len(points)):

            for j in range(i+1, len(self.route)):
                if(lines_intersect(points[i-1], points[i], points[j], points[j-1])):
                    intersects = True

        return intersects

    def lines_intersect(point_1, point_2, point_3, point_4):
        return False


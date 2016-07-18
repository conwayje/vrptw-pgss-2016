# Jahnik and Dan
# Simple class to interact with a route/path of a truck
# Can return the total distance, customer at a certain time ..
# c was used as customer in order to avoid conflict with old code

import math
from Distances import Distances

class Path():

    def __init__(self, route):
        self.route = route #list of customers
        self.distance = self.calculate_distance()

    # returns the total distance
    def calculate_distance(self):

        prev_customer = self.route[0]
        distance = Distances.get_distance(0, prev_customer.number)

        for c in self.route[1:]:
            distance += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

        distance += Distances.get_distance(prev_customer.number, 0)


        return distance

    def get_arrival_time_of_customer(self, cust):
        """Returns the time at which the truck on this path arrives at this customer
        given the order of customers prior to the given customer and their windows"""

        prev_customer = self.route[0]
        time = Distances.get_distance(prev_customer.number, 0)

        if time < prev_customer.open_time:
            time = prev_customer.open_time


        if prev_customer == cust:
            return time

        for c in self.route[1:]:

            time += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

            # if truck arrives before customer is open, assume truck waits
            if time < c.open_time:
                time = c.open_time

            if (c == cust):
                return time

            time += c.service_time


        return -1

    def is_valid(self):
        # @TODO -- just a note: comments before a function aren't "part of python" in any really meaningful ways.
        # if you do it like this -- called a docstring -- then you can actually access this information while you're
        # using a python interpreter and such, which can be very convenient.
        #
        # you don't need to do anything here; just a note for the future
        """returns whether the truck makes it on time to every customer by returning
        an array of the customers missed. If the path is valid, an empty array will be returned"""

        prev_customer = self.route[0]
        time = Distances.get_distance(prev_customer.number,0)

        missedCustomers = []

        # if truck arrives before customer is open, assume truck waitds
        if time < prev_customer.open_time:
            time = prev_customer.open_time

        # if truck arrives late, add to missedCustomers
        if time > prev_customer.close_time:
            missedCustomers.append(prev_customer)

        time += prev_customer.service_time

        for c in self.route[1:]:
            time += Distances.get_distance(prev_customer.number, c.number)
            prev_customer = c

            # if truck arrives before customer is open, assume truck waitds
            if time < c.open_time:
                #
                time = c.open_time

            # if truck arrives late, add to missedCustomers
            if time > c.close_time:
                missedCustomers.append(c)

            time += c.service_time
        # @TODO -- the name is_valid makes me expect this would return at least a boolean value
        # [and perhaps something else in addition]
        # maybe we should return True/False, missedCustomers instead?
        return missedCustomers

    # gets the customer the truck was last at
    def get_last_customer_visited(self, current_time):
        prev_customer = self.route[0]

        time = Distances.get_distance(prev_customer.number, 0)
        if (time > current_time):
            return None

        # if truck arrives before customer is open, assume truck waits
        if time < prev_customer.open_time:
            time = prev_customer.open_time
        time += prev_customer.service_time

        if (time > current_time):
            return prev_customer

        for c in self.route[1:]:

            time += Distances.get_distance(prev_customer.number, c.number)

            if(time > current_time):
                return prev_customer

            # if truck arrives before customer is open, assume truck waitds
            if time < c.open_time:
                time = c.open_time
            time += c.service_time

            if(time > current_time):
                return c

            prev_customer = c
        return None

    # returns whether the path intersects itself
    def intersects_self(self):
        intersects = 0
        points = [(0, 0)]
        for c in self.route:
            points.append((c.x, c.y))

        points.append((0,0))

        for i in range(1, len(points)):
            for j in range(i + 1, len(self.route)):
                if (Path.lines_intersect(points[i - 1], points[i], points[j], points[j - 1])):
                    intersects += 1

        return intersects

    # Will probably be used for inserting in completed solutions for clusters
    def append(self, toAppend):
        self.route.append(toAppend.route)

    # Will probably be used for inserting in completed solutions for clusters
    def insert(self, toAppend, index):
        for c in toAppend.route:
            self.insert(index, c)
            index += 1


    # Given two lines AB and CD, determines if they intersect
    # If
    # source http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    @staticmethod
    def lines_intersect(A, B, C, D):
        return Path.ccw(A,C,D) != Path.ccw(B,C,D) and Path.ccw(A,B,C) != Path.ccw(A,B,D)

    # helper method for lines_intersect()
    @staticmethod
    def ccw(A, B, C):
        # @TODO -- there's a liiiiittle bit too much magic happening here.  so what is
        # "A" exactly, and what does the assignment do?
        #
        # might want to add a docstring describing the structure of the arguments; it's not
        # immediately obvious what it's expecting
        (Ax, Ay) = A
        (Bx, By) = B
        (Cx, Cy) = C
        return (Cy - Ay) * (Bx - Ax) > (By - Ay) * (Cx - Ax)

    def distance_to_previous(self, customer):
        index = self.route.index(customer) - 1
        if index >= 0:
            return Distances.get_distance(customer.number, self.route[index].number)
        else:
            return Distances.get_distance(customer.number, 0)

    def distance_to_next(self, customer):
        index = self.route.index(customer) + 1
        if index < len(self.route):
            return Distances.get_distance(customer.number, self.route[index].number)
        else:
            return Distances.get_distance(customer.number, 0)

    def cargo_used(self, customer=None):
        result = 0
        for cust in self.route:
            result += customer.demand
            if customer == cust:
                return result
        return result

    def get_indice_customer_missed(self, cargo):
        ''':return the indice of the first customer missed, will return -1 if makes it '''
        indice = 0
        cargo_used = 0
        for cust in self.route:
            if cargo_used > cargo:
                return indice
            cargo_used += cust.cargo
            indice += 1
        return -1


    def __repr__(self):
        # return "<Path: {0}>".format(self.route)
        return "<Path: {}>".format([customer.number for customer in self.route])

